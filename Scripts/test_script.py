

def print_last_operation(vm_store):
    vm = vm_store.get("Calculator")
    if not vm:
        print("❌ Calculator view model not found")
        return

    try:
        a = getattr(vm, "a", None)
        b = getattr(vm, "b", None)
        op = getattr(vm, "operation", None)
        res = getattr(vm, "result", None)

        if None in (a, b, op, res):
            print("⚠️ Some values are missing.")
        else:
            print(f"{a} {op} {b} = {res}")

    except Exception as e:
        print(f"❌ Error: {e}")

print("Hello world!")
print_last_operation(vm_store)
