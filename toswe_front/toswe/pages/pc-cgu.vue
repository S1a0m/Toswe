<template>
  <section class="min-h-screen bg-[#fdf8f5] py-12 px-4">
    <div class="max-w-6xl mx-auto grid lg:grid-cols-4 gap-10">
      <!-- Sommaire -->
      <aside class="lg:col-span-1 hidden lg:block">
        <div class="sticky top-20 bg-white rounded-xl shadow p-6">
          <h2 class="text-lg font-bold text-[#7D260F] mb-4">📑 Sommaire</h2>
          <nav class="space-y-2 text-sm">
            <a href="#privacy" class="block text-gray-700 hover:text-[#7D260F]">
              🔐 Politique de confidentialité
            </a>
            <ul class="pl-4 space-y-1 text-gray-500">
              <li><a href="#privacy-data" class="hover:text-[#7D260F]">1. Données collectées</a></li>
              <li><a href="#privacy-use" class="hover:text-[#7D260F]">2. Utilisation</a></li>
              <li><a href="#privacy-share" class="hover:text-[#7D260F]">3. Partage</a></li>
              <li><a href="#privacy-security" class="hover:text-[#7D260F]">4. Sécurité</a></li>
              <li><a href="#privacy-rights" class="hover:text-[#7D260F]">5. Vos droits</a></li>
            </ul>
            <a href="#terms" class="block mt-4 text-gray-700 hover:text-[#7D260F]">
              📜 Conditions d’utilisation
            </a>
            <ul class="pl-4 space-y-1 text-gray-500">
              <li><a href="#terms-object" class="hover:text-[#7D260F]">1. Objet</a></li>
              <li><a href="#terms-account" class="hover:text-[#7D260F]">2. Compte</a></li>
              <li><a href="#terms-products" class="hover:text-[#7D260F]">3. Produits</a></li>
              <li><a href="#terms-payments" class="hover:text-[#7D260F]">4. Paiements</a></li>
              <li><a href="#terms-delivery" class="hover:text-[#7D260F]">5. Livraison</a></li>
              <li><a href="#terms-responsibility" class="hover:text-[#7D260F]">6. Responsabilités</a></li>
              <li><a href="#terms-suspension" class="hover:text-[#7D260F]">7. Suspension</a></li>
              <li><a href="#terms-modifications" class="hover:text-[#7D260F]">8. Modifications</a></li>
            </ul>
          </nav>
        </div>
      </aside>

      <!-- Contenu -->
      <main class="lg:col-span-3 bg-white shadow-xl rounded-2xl p-8 sm:p-12">
        <!-- Politique -->
        <header id="privacy" class="mb-10 text-center">
          <h1 class="text-3xl sm:text-4xl font-extrabold text-[#7D260F] mb-2">
            🔐 Politique de confidentialité – Tôswè
          </h1>
          <p class="text-sm text-gray-500">Dernière mise à jour : 25 septembre 2025</p>
        </header>

        <div class="prose prose-lg max-w-none text-gray-700">
          <p>
            Chez <strong>Tôswè</strong>, nous attachons une grande importance à
            la protection de vos données personnelles.
          </p>

          <h2 id="privacy-data">1. Données que nous collectons</h2>
          <ul>
            <li>Nom, prénom et numéro de téléphone.</li>
            <li>Adresse de livraison et informations de paiement.</li>
            <li>Produits consultés, commandés ou vendus.</li>
            <li>Données techniques (cookies, adresse IP, logs).</li>
          </ul>

          <h2 id="privacy-use">2. Utilisation des données</h2>
          <ul>
            <li>Créer et gérer votre compte.</li>
            <li>Permettre achats, ventes et livraisons.</li>
            <li>Améliorer l’expérience utilisateur.</li>
            <li>Envoyer des notifications (commandes, promos, mises à jour).</li>
          </ul>

          <h2 id="privacy-share">3. Partage des données</h2>
          <p>
            Nous ne vendons jamais vos données. Elles peuvent être partagées
            uniquement avec :
          </p>
          <ul>
            <li>Les vendeurs (commandes).</li>
            <li>Les livreurs (livraisons).</li>
            <li>Les partenaires techniques (support plateforme).</li>
          </ul>

          <h2 id="privacy-security">4. Sécurité</h2>
          <p>
            Nous mettons en place des mesures techniques et organisationnelles
            pour protéger vos données contre tout accès non autorisé.
          </p>

          <h2 id="privacy-rights">5. Vos droits</h2>
          <ul>
            <li>Accéder, rectifier ou supprimer vos données.</li>
            <li>Retirer votre consentement à tout moment.</li>
          </ul>
          <p>
            Contact : 
            <a href="mailto:support@toswe.com" class="text-[#7D260F] underline">
              support@toswe.com
            </a>
          </p>
        </div>

        <!-- Séparateur -->
        <div class="my-12 border-t border-gray-200"></div>

        <!-- Conditions -->
        <header id="terms" class="mb-10 text-center">
          <h1 class="text-3xl sm:text-4xl font-extrabold text-[#7D260F] mb-2">
            📜 Conditions d’utilisation – Tôswè
          </h1>
          <p class="text-sm text-gray-500">Dernière mise à jour : 25 septembre 2025</p>
        </header>

        <div class="prose prose-lg max-w-none text-gray-700">
          <h2 id="terms-object">1. Objet</h2>
          <p>
            Tôswè permet aux commerçants locaux de vendre et aux clients
            d’acheter avec livraison simplifiée.
          </p>

          <h2 id="terms-account">2. Création et gestion de compte</h2>
          <ul>
            <li>Connexion via numéro + OTP.</li>
            <li>Données exactes obligatoires.</li>
            <li>Compte personnel et non transférable.</li>
          </ul>

          <h2 id="terms-products">3. Produits autorisés</h2>
          <ul>
            <li>Produits <strong>Made in Bénin / Made in Africa</strong> uniquement.</li>
            <li>Interdits : contrefaçons, produits dangereux ou illégaux.</li>
          </ul>

          <h2 id="terms-payments">4. Commandes et paiements</h2>
          <ul>
            <li>Espèces ou mobile money acceptés.</li>
            <li>Commission sur chaque vente.</li>
          </ul>

          <h2 id="terms-delivery">5. Livraison</h2>
          <ul>
            <li>Effectuée par Tôswè ou partenaires.</li>
            <li>Délai indicatif, non garanti à 100%.</li>
          </ul>

          <h2 id="terms-responsibility">6. Responsabilités</h2>
          <ul>
            <li>Tôswè agit comme intermédiaire.</li>
            <li>Le vendeur est responsable des produits.</li>
            <li>L’acheteur est responsable des infos de livraison.</li>
          </ul>

          <h2 id="terms-suspension">7. Suspension ou résiliation</h2>
          <p>
            Compte suspendu/supprimé en cas de fraude, vente de produits interdits ou non-respect.
          </p>

          <h2 id="terms-modifications">8. Modifications</h2>
          <p>
            Nous pouvons mettre à jour ces conditions avec notification en cas
            de changements majeurs.
          </p>
        </div>
      </main>
    </div>
  </section>
</template>
