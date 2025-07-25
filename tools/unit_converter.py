def convert_units(message):
    try:
        if "m ke cm" in message or "meter ke senti" in message:
            angka = int("".join(filter(str.isdigit, message)))
            return f"{angka} meter = {angka * 100} cm"
        elif "cm ke m" in message:
            angka = int("".join(filter(str.isdigit, message)))
            return f"{angka} cm = {angka / 100} meter"
        else:
            return "Kamu mau konversi apa nih? Contoh: konversi 100m ke cm"
    except:
        return "Format konversinya nggak jelas, coba ketik ulang yaa 🥺"
