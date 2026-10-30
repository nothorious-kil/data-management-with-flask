import os
import shutil
import sqlite3
from pathlib import Path
from tempfile import gettempdir

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
PROJECT_DIR = Path(__file__).resolve().parent
SAMPLE_DATABASE = PROJECT_DIR / "etudiants.db"

if os.environ.get("VERCEL"):
    DATABASE_PATH = Path(gettempdir()) / "etudiants.db"
    if not DATABASE_PATH.exists() and SAMPLE_DATABASE.exists():
        shutil.copy2(SAMPLE_DATABASE, DATABASE_PATH)
else:
    DATABASE_PATH = SAMPLE_DATABASE


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS etudiants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            classe TEXT NOT NULL,
            note REAL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db_connection()
    etudiants = conn.execute("SELECT * FROM etudiants ORDER BY nom").fetchall()
    conn.close()
    return render_template("index.html", etudiants=etudiants)


@app.route("/ajouter", methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        classe = request.form["classe"]
        note = request.form["note"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO etudiants (nom, prenom, classe, note) VALUES (?, ?, ?, ?)",
            (nom, prenom, classe, note),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("ajouter.html")


@app.route("/modifier/<int:id>", methods=["GET", "POST"])
def modifier(id):
    conn = get_db_connection()
    etudiant = conn.execute("SELECT * FROM etudiants WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        classe = request.form["classe"]
        note = request.form["note"]

        conn.execute(
            "UPDATE etudiants SET nom=?, prenom=?, classe=?, note=? WHERE id=?",
            (nom, prenom, classe, note, id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("modifier.html", etudiant=etudiant)


@app.route("/supprimer/<int:id>")
def supprimer(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM etudiants WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


init_db()


if __name__ == "__main__":
    app.run(debug=True)
