import inspect

from abc import ABC
from typing import Any, Dict, Callable, List, Optional
from inspect import getfullargspec
from Illuminate.Helpers.Util import Util
from Illuminate.Support.builtins import array_merge


class AttributeNotFound(Exception):
    pass


class BindingNotFound(Exception):
    pass


class BindingResolutionException(Exception):
    pass


class BuildingNewInstanceRequired(Exception):
    pass


class Container(ABC):
    def __init__(self) -> None:
        self.__bindings: Dict[str, Dict[str, Any]] = {}
        self.__instances: Dict[str, Any] = {}
        self.__resolved: Dict[str, bool] = {}
        self.__aliases: Dict[str, str] = {}
        self.__abstract_aliases: Dict[str, list] = {}
        self.__contextual_bindings: Dict[Any, Dict[Any, Any]] = {}
        self.__build_stack: list = []
        self.__extenders: Dict[Any, list] = {}
        self.__tags: Dict[Any, list] = {}
        self.__rebound_callbacks: Dict[Any, list] = {}
        self._global_before_resolving_callbacks: list = []
        self._before_resolving_callbacks: dict = {}
        self._global_resolving_callbacks: list = []
        self._resolving_callbacks: dict = {}
        self._global_after_resolving_callbacks: list = []
        self._after_resolving_callbacks: dict = {}

    def bind(self, key: str, binding_resolver: Callable) -> None:
        self.__bind(key, binding_resolver, False)

    def singleton(self, key: str, binding_resolver: Callable) -> None:
        self.__bind(key, binding_resolver, True)

    def when(self, concrete):
        from Illuminate.Container.ContextualBindingBuilder import (
            ContextualBindingBuilder,
        )

        return ContextualBindingBuilder(self, concrete)

    def add_contextual_binding(self, concrete, abstract, implementation):
        concrete = self.get_alias(concrete)
        abstract = self.get_alias(abstract)
        self.__contextual_bindings.setdefault(concrete, {})[abstract] = implementation

    def make(self, key: str, parameters: Dict[str, Any] = {}) -> Any:
        assert isinstance(parameters, dict), "Parameters must be key, value"

        return self.resolve(key, parameters)

    def resolve(
        self,
        abstract: str,
        parameters: Dict[str, Any] = {},
    ):
        abstract = self.get_alias(abstract)

        self._fire_before_resolving_callbacks(abstract, parameters)

        concrete = self._get_contextual_concrete(abstract, parameters)

        needs_contextual_builds = parameters or concrete

        instance = self.get_instance(abstract)

        if instance and not needs_contextual_builds:
            return instance

        if not concrete:
            concrete = self._get_concrete(abstract, parameters)

        self._fire_resolving_callbacks(abstract, concrete)

        return concrete

    def _get_contextual_concrete(self, abstract: str, parameters: Dict[str, Any] = {}):
        binding = self._find_in_contextual_bindings(abstract, parameters)

        if binding:
            return binding

        abstract_aliases = self.__abstract_aliases.get(abstract)

        if not abstract_aliases:
            return None

        for alias in abstract_aliases:
            binding = self._find_in_contextual_bindings(alias, parameters)

            if binding:
                return binding

    def _fire_before_resolving_callbacks(
        self, abstract: str, parameters: Dict[str, Any] = {}
    ):
        self._fire_before_callback_array(
            abstract, parameters, self._global_before_resolving_callbacks
        )

        for type, callbacks in self._before_resolving_callbacks.items():
            if type == abstract or (
                inspect.isclass(type)
                and inspect.isclass(abstract)
                and issubclass(type, abstract)
            ):
                self._fire_before_callback_array(abstract, parameters, callbacks)

    def _fire_before_callback_array(self, abstract, parameters, callbacks):
        for callback in callbacks:
            Util.callback_with_dynamic_args(callback, [abstract, parameters, self])

    def _fire_resolving_callbacks(self, abstract, concrete):
        self._fire_callback_array(concrete, self._global_resolving_callbacks)

        self._fire_callback_array(
            concrete,
            self._get_callbacks_for_type(abstract, concrete, self._resolving_callbacks),
        )

        self._fire_after_resolving_callbacks(abstract, concrete)

    def _fire_after_resolving_callbacks(self, abstract, concrete):
        self._fire_callback_array(concrete, self._global_after_resolving_callbacks)

        self._fire_callback_array(
            concrete,
            self._get_callbacks_for_type(
                abstract, concrete, self._after_resolving_callbacks
            ),
        )

    def _get_callbacks_for_type(self, abstract, concrete, callbacks_per_type):
        results = []

        for type, callbacks in callbacks_per_type.items():
            if type == abstract or (
                inspect.isclass(type) and isinstance(concrete, type)
            ):
                results = array_merge(results, callbacks)

        return results

    def _fire_callback_array(self, concrete, callbacks):
        for callback in callbacks:
            Util.callback_with_dynamic_args(callback, [concrete, self])

    def before_resolving(self, abstract, callback=None):
        if isinstance(abstract, str):
            abstract = self.get_alias(abstract)

        if callable(abstract) and not callback:
            self._global_before_resolving_callbacks.append(abstract)
        else:
            self._before_resolving_callbacks.setdefault(abstract, []).append(callback)

    def resolving(self, abstract, callback=None):
        if isinstance(abstract, str):
            abstract = self.get_alias(abstract)

        if callable(abstract) and not callback:
            self._global_resolving_callbacks.append(abstract)
        else:
            self._resolving_callbacks.setdefault(abstract, []).append(callback)

    def after_resolving(self, abstract, callback=None):
        if isinstance(abstract, str):
            abstract = self.get_alias(abstract)

        if callable(abstract) and not callback:
            self._global_after_resolving_callbacks.append(abstract)
        else:
            self._after_resolving_callbacks.setdefault(abstract, []).append(callback)

    def bind_if(self, key: str, binding_resolver: Callable) -> None:
        if not self.bound(key):
            self.__bind(key, binding_resolver, False)

    def bound(self, abstract: str) -> bool:
        return (
            abstract in self.__bindings
            or abstract in self.__instances
            or abstract in self.__aliases
        )

    def instance(self, abstract: str, instance: Any) -> Any:
        abstract = self.get_alias(abstract)
        was_bound = self.bound(abstract)
        result = self.__make_instance(abstract, instance)

        if was_bound:
            self._rebound(abstract)

        return result

    def alias(self, abstract: str, alias: str) -> None:
        if abstract == alias:
            raise Exception(f"{abstract} cannot alias itself")

        self.__aliases[alias] = abstract
        self.__abstract_aliases.setdefault(abstract, []).append(alias)

    def get_alias(self, abstract: Any) -> Any:
        return (
            self.get_alias(self.__aliases.get(abstract))
            if abstract in self.__aliases
            else abstract
        )

    def get_aliases(self) -> Dict[str, str]:
        return self.__aliases

    def get_abstract_aliases(self) -> Dict[str, list]:
        return self.__abstract_aliases

    def get_bindings(self) -> Dict[str, Dict[str, Any]]:
        return self.__bindings

    def get_instance(self, key: str) -> Optional[Any]:
        return self.__instances.get(key)

    def get_instances(self) -> Dict[str, Any]:
        return self.__instances

    def get_resolved(self) -> Dict[str, bool]:
        return self.__resolved

    def extend(self, abstract, extender):
        abstract = self.get_alias(abstract)

        if abstract in self.__instances:
            self.__instances[abstract] = extender(
                self.__instances[abstract],
                self,
            )
            self._rebound(abstract)
            return

        self.__extenders.setdefault(abstract, []).append(extender)

        if self.resolved(abstract):
            self._rebound(abstract)

    def tag(self, abstracts, *tags):
        for tag in tags:
            self.__tags.setdefault(tag, []).extend(
                abstract for abstract in (abstracts if isinstance(abstracts, list) else [abstracts])
            )

    def tagged(self, tag):
        return [self.make(abstract) for abstract in self.__tags.get(tag, [])]

    def rebinding(self, abstract, callback):
        abstract = self.get_alias(abstract)
        self.__rebound_callbacks.setdefault(abstract, []).append(callback)

        if self.bound(abstract):
            return self.make(abstract)

    def _rebound(self, abstract):
        callbacks = self.__rebound_callbacks.get(abstract, [])
        if not callbacks:
            return

        instance = self.make(abstract)
        for callback in callbacks:
            callback(self, instance)

    def __bind(self, abstract: str, binding_resolver: Callable, shared: bool) -> None:
        abstract = self.get_alias(abstract)

        self.__bindings[abstract] = {
            "abstract": abstract,
            "binding_resolver": binding_resolver,
            "shared": shared,
        }

        if self.resolved(abstract):
            self._rebound(abstract)

    def __make_instance(self, abstract: str, instance: Any) -> Any:
        self.__instances[abstract] = instance
        return instance

    def _find_in_contextual_bindings(
        self, abstract: str, parameters: List[Any] = []
    ) -> Optional[Any]:
        if self.__build_stack:
            concrete = self.__build_stack[-1]
            implementation = self.__contextual_bindings.get(concrete, {}).get(abstract)
            if implementation is not None:
                return self.__resolve(abstract, implementation, parameters)

        binding = self.__bindings.get(abstract)
        if not binding:
            return None

        binding_resolver = binding["binding_resolver"]
        shared = binding["shared"]

        if shared and (abstract in self.__instances):
            return self.__instances[abstract]

        instance = self.__resolve(abstract, binding_resolver, parameters)

        if shared:
            self.__instances[abstract] = instance

        return instance

    def _get_concrete(self, abstract: str, parameters: Dict[str, Any] = {}) -> Any:
        try:
            return self.__resolve(abstract, abstract, parameters)
        except BindingResolutionException as e:
            raise e

    def __resolve(
        self, abstract: str, binding_resolver: Any, parameters: Dict[str, Any] = {}
    ) -> Any:
        self.__build_stack.append(abstract)
        try:
            args = getfullargspec(binding_resolver).args
            dependencies = self.get_dependencies(binding_resolver, parameters)

            instance = Util.callback_with_dynamic_args(binding_resolver, dependencies)
            for extender in self.__extenders.get(abstract, []):
                instance = extender(instance, self)

            if instance:
                self.__resolved[abstract] = True
                return instance

            raise BindingResolutionException(
                f"Binding Resolution Exception for key {abstract} and class {binding_resolver}"
            )
        finally:
            self.__build_stack.pop()

    def get_dependencies(
        self,
        class_info,
        parameters: Dict[str, Any] | None = None,
    ) -> List[Any]:
        parameters = parameters or {}
        args_info = getfullargspec(class_info)
        dependencies = []
        defaults = dict(
            zip(
                args_info.args[-len(args_info.defaults):],
                args_info.defaults,
            )
        ) if args_info.defaults else {}

        for argument in args_info.args:
            if argument == "self":
                continue

            if argument in parameters:
                dependencies.append(parameters[argument])
                continue

            annotation = args_info.annotations.get(argument)
            if annotation is None:
                if argument in defaults:
                    dependencies.append(defaults[argument])
                    continue
                raise BindingResolutionException(
                    f"Unresolvable dependency [{argument}] for {class_info}"
                )

            try:
                dependencies.append(self.make(annotation))
            except (TypeError, BindingResolutionException) as error:
                if argument in defaults:
                    dependencies.append(defaults[argument])
                    continue
                raise BindingResolutionException(
                    f"Unresolvable dependency [{annotation}] for {class_info}"
                ) from error

        return dependencies

    def get_resolved_dependencies(self, abstract: str) -> Dict[str, Any]:
        if abstract not in self.__resolved:
            raise BindingResolutionException(f"{abstract} is not resolved")

        return {abstract: self.__instances.get(abstract)}

    def clear_resolved(self) -> None:
        self.__resolved.clear()

    def has(self, abstract: str) -> bool:
        return self.bound(abstract)
    def resolved(self, abstract: str) -> bool:
        abstract = self.get_alias(abstract)
        return abstract in self.__resolved or abstract in self.__instances

    def is_shared(self, abstract: str) -> bool:
        abstract = self.get_alias(abstract)

        if abstract in self.__instances:
            return True

        binding = self.__bindings.get(abstract)
        return bool(binding and binding["shared"])

    def forget_instance(self, abstract: str) -> None:
        abstract = self.get_alias(abstract)

        if abstract in self.__instances:
            del self.__instances[abstract]

    def forget_binding(self, abstract: str) -> None:
        abstract = self.get_alias(abstract)

        if abstract in self.__bindings:
            del self.__bindings[abstract]

        self.forget_instance(abstract)

    def flush(self) -> None:
        self.__bindings.clear()
        self.__instances.clear()
        self.__resolved.clear()
        self.__aliases.clear()
        self.__abstract_aliases.clear()
