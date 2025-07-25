
def convert_units(query):
    try:
        import pint
        ureg = pint.UnitRegistry()
        value, _, unit_from, _, unit_to = query.lower().split()
        result = ureg.Quantity(float(value), unit_from).to(unit_to)
        return f"{value} {unit_from} = {result}"
    except Exception as e:
        return f"Konversi gagal: {e}"

