from flask import Flask, render_template, request, redirect, session
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = "123456"

# "banco" simples
horarios = []
agendamentos = []

# login admin
USER = "admin"
PASS = "123"


# ======================
# CLIENTE
# ======================
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        servico = request.form.get("servico")
        horario_id = int(request.form.get("horario"))

        for h in horarios:
            if h["id"] == horario_id and h["disponivel"]:
                h["disponivel"] = False

                agendamentos.append({
                    "nome": nome,
                    "telefone": telefone,
                    "servico": servico,
                    "horario": h
                })

                msg = f"""💅 Novo agendamento - Salão da Nem

👤 Cliente: {nome}
📞 Telefone: {telefone}

💅 Serviço: {servico}

📅 Data: {h['data']}
⏰ Hora: {h['hora']}"""

                numero = "5531991668862"  # SEU WHATSAPP
                link = f"https://wa.me/{numero}?text={quote(msg)}"

                return render_template(
                    "confirmacao.html",
                    nome=nome,
                    data=h["data"],
                    hora=h["hora"],
                    servico=servico,
                    link=link
                )

    horarios_disp = [h for h in horarios if h["disponivel"]]

    return render_template("home.html", horarios=horarios_disp)


# ======================
# LOGIN ADMIN
# ======================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")

        if user == USER and password == PASS:
            session["admin"] = True
            return redirect("/admin")

    return render_template("admin_login.html")


# ======================
# PAINEL ADMIN
# ======================
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect("/admin/login")

    if request.method == "POST":
        data = request.form.get("data")
        hora = request.form.get("hora")

        new_id = len(horarios) + 1

        horarios.append({
            "id": new_id,
            "data": data,
            "hora": hora,
            "disponivel": True
        })

    return render_template("admin.html", horarios=horarios, agendamentos=agendamentos)


# ======================
# REMOVER HORÁRIO
# ======================
@app.route("/remover/<int:id>")
def remover(id):
    if not session.get("admin"):
        return redirect("/admin/login")

    global horarios
    horarios = [h for h in horarios if h["id"] != id]

    return redirect("/admin")


# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/admin/login")


# ======================
# RODAR APP
# ======================
if __name__ == "__main__":
    app.run(debug=True)