import dash.hooks as hooks
from datetime import timedelta, time


def test_setup_hook():
    """
    Verify that the setup hook assigns the correct metadata to the callback function.
    """
    @hooks.setup
    def test_callback():
        return 2 + 2

    assert hasattr(test_callback, hooks.ATTRIBUTE_NAME)

    hook = getattr(test_callback, hooks.ATTRIBUTE_NAME)
    assert isinstance(hook, hooks.ScriptHook)
    assert hook.callback == test_callback
    assert hook.event == hooks.HookEvent.Setup


def test_schedule_hook():
    """
    Verify that the schedule hooks assigns the correct metadata to the callback function.
    """
    @hooks.schedule(run_every=timedelta(days=1), at=time(hour=12, minute=0))
    def test_callback():
        return 2 + 2

    assert hasattr(test_callback, hooks.ATTRIBUTE_NAME)

    hook = getattr(test_callback, hooks.ATTRIBUTE_NAME)
    assert isinstance(hook, hooks.ScriptHook)
    assert hook.callback == test_callback
    assert hook.event == hooks.HookEvent.Entry

    assert hook.schedule.run_every == timedelta(days=1)
    assert hook.schedule.run_at == time(hour=12, minute=0)


# TODO: Test that parameters are ignored under conditions specified in documentation


def test_hook_func_callable():
    """
    Verify that a callback function is still usable if run from outside of the context
    of this project. In other words, the hook decorators shouldn't prevent a user from
    using the function independent of the script scheduler.
    """
    @hooks.setup
    def test_callback(name):
        return "Hello {0}".format(name)

    assert test_callback("Mark") == "Hello Mark"


def test_duplicate_hooks():
    """
    Applying the same decorator twice should be equivalent to applying it once.
    """
    @hooks.setup
    @hooks.setup
    def test_callback():
        pass

    hook = getattr(test_callback, hooks.ATTRIBUTE_NAME)
    assert hook.callback == test_callback
    assert hook.event == hooks.HookEvent.Setup


# TODO: add support for multiple hooks and test

# TODO: test load_hooks()
