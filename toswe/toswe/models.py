from django.db import models
from django.contrib.auth.models import AbstractUser


# ========================
# Utilisateur personnalisé
# ========================
class Utilisateur(AbstractUser):
    TYPE_CHOIX = [
        ('client', 'Client'),
        ('vendeur', 'Vendeur'),
        ('admin', 'Administrateur'),
    ]
    type_utilisateur = models.CharField(max_length=10, choices=TYPE_CHOIX, default='client')
    id_racine = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.id_racine


# ==========
# Catégorie
# ==========
class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom


# ========
# Produit
# ========
class Produit(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.PositiveIntegerField()
    image_url = models.URLField(blank=True)
    etat = models.CharField(max_length=20, default="disponible")

    vendeur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='produits')
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nom


# =========
# Commande
# =========
class Commande(models.Model):
    STATUT_CHOIX = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='en_attente')
    adresse_livraison = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Commande #{self.id} - {self.utilisateur.username}"


# =================
# Ligne de commande
# =================
class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def sous_total(self):
        return self.quantite * self.prix_unitaire


# ==========
# Paiement
# ==========
class Paiement(models.Model):
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE)
    moyen = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=30)
    montant = models.DecimalField(max_digits=10, decimal_places=2)


# ==========
# Livraison
# ==========
class Livraison(models.Model):
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE)
    statut = models.CharField(max_length=30)
    transporteur = models.CharField(max_length=100, blank=True)
    num_suivi = models.CharField(max_length=100, blank=True)
    date_envoi = models.DateField(null=True, blank=True)
    date_livraison = models.DateField(null=True, blank=True)


# ==========
# Avis produit
# ==========
class AvisProduit(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='avis')
    note = models.IntegerField()
    commentaire = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.note}/5 par {self.utilisateur.username}"
