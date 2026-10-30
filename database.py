# database.py

# On importe sqlite3 pour utiliser une base de données SQLite.
import sqlite3

# Nom du fichier de base de données.
NOM_BASE = "etudiants.db"


def obtenir_connexion():
    """
    Ouvre une connexion avec la base de données.

    row_factory permet de récupérer les résultats
    comme des dictionnaires.

    Exemple :
    etudiant["nom"]

    au lieu de :
    etudiant[1]
    """

    connexion = sqlite3.connect(NOM_BASE)

    # Permet d'accéder aux colonnes avec leur nom.
    connexion.row_factory = sqlite3.Row

    return connexion


def initialiser_base():
    """
    Crée la table étudiants si elle n'existe pas encore.
    """

    connexion = obtenir_connexion()

    connexion.execute("""
        CREATE TABLE IF NOT EXISTS etudiants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            classe TEXT NOT NULL,
            note REAL NOT NULL
        )
    """)

    # On valide la création de la table.
    connexion.commit()

    # On ferme la connexion.
    connexion.close()


def obtenir_tous_les_etudiants():
    """
    Récupère tous les étudiants dans la base de données.
    """

    connexion = obtenir_connexion()

    etudiants = connexion.execute("""
        SELECT *
        FROM etudiants
        ORDER BY nom ASC
    """).fetchall()

    connexion.close()

    return etudiants


def obtenir_un_etudiant(id_etudiant):
    """
    Récupère un seul étudiant grâce à son identifiant.
    """

    connexion = obtenir_connexion()

    etudiant = connexion.execute(
        """
        SELECT *
        FROM etudiants
        WHERE id = ?
    """,
        (id_etudiant,),
    ).fetchone()

    connexion.close()

    return etudiant


def ajouter_etudiant(nom, prenom, classe, note):
    """
    Ajoute un nouvel étudiant dans la base.
    """

    connexion = obtenir_connexion()

    connexion.execute(
        """
        INSERT INTO etudiants (nom, prenom, classe, note)
        VALUES (?, ?, ?, ?)
    """,
        (nom, prenom, classe, note),
    )

    connexion.commit()
    connexion.close()


def modifier_etudiant(id_etudiant, nom, prenom, classe, note):
    """
    Modifie les informations d'un étudiant existant.
    """

    connexion = obtenir_connexion()

    connexion.execute(
        """
        UPDATE etudiants
        SET nom = ?,
            prenom = ?,
            classe = ?,
            note = ?
        WHERE id = ?
    """,
        (nom, prenom, classe, note, id_etudiant),
    )

    connexion.commit()
    connexion.close()


def supprimer_etudiant(id_etudiant):
    """
    Supprime un étudiant grâce à son identifiant.
    """

    connexion = obtenir_connexion()

    connexion.execute(
        """
        DELETE FROM etudiants
        WHERE id = ?
    """,
        (id_etudiant,),
    )

    connexion.commit()
    connexion.close()
