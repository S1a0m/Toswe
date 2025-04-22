import 'dart:ui';
import 'package:flutter/material.dart';

class ProfileView extends StatelessWidget {
  const ProfileView({super.key});

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // 🎨 Image de fond
        Container(
          decoration: const BoxDecoration(
            image: DecorationImage(
              image: AssetImage("assets/toswe-africa-art.png"),
              fit: BoxFit.cover,
            ),
          ),
        ),

        // 💎 Flou général
        BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 8, sigmaY: 8),
          child: Container(
            color: Colors.black.withOpacity(0),
          ),
        ),

        // 📋 Contenu
        SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              children: [
                // --- Avatar ---
                Container(
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.2),
                        blurRadius: 10,
                        offset: const Offset(0, 5),
                      ),
                    ],
                  ),
                  child: const CircleAvatar(
                    radius: 50,
                    backgroundColor: Color(0xFFC0A080),
                    child: Icon(Icons.person, size: 60, color: Colors.white),
                  ),
                ),
                const SizedBox(height: 12),

                // --- Statut ---
                const Text(
                  "Profile • Client",
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFFC0A080),
                    /*shadows: [
                      Shadow(
                        color: Colors.white70,
                        blurRadius: 4,
                        offset: Offset(1, 1),
                      )
                    ],*/
                  ),
                ),
                const SizedBox(height: 24),

                // --- Carte d'information utilisateur ---
                _glassInfoCard([
                  _buildInfoRow(Icons.person, "Nom", "Jean Dupont"),
                  _buildInfoRow(Icons.phone, "Téléphone", "+33 6 12 34 56 78"),
                  _buildInfoRow(
                      Icons.location_on, "Adresse", "12 rue des Lilas, Paris"),
                ]),

                const Spacer(),

                // --- Bouton Modifier ---
                Align(
                  alignment: Alignment.centerRight,
                  child: TextButton(
                    onPressed: () {
                      // Action de modification ici
                    },
                    child: const Text(
                      "Modifier →",
                      style: TextStyle(
                        color: Color(0xFFC0A080),
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  // --- Carte de présentation floutée (Glass)
  Widget _glassInfoCard(List<Widget> children) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(16),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 6, sigmaY: 6),
        child: Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          margin: const EdgeInsets.symmetric(horizontal: 0),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.25),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.white.withOpacity(0.2)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children:
                children.expand((e) => [e, const SizedBox(height: 12)]).toList()
                  ..removeLast(), // Pour éviter le dernier espace
          ),
        ),
      ),
    );
  }

  // --- Ligne d'information utilisateur
  Widget _buildInfoRow(IconData icon, String label, String value) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, color: Color(0xFFC0A080)),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 14,
                  )),
              const SizedBox(height: 2),
              Text(value,
                  style: const TextStyle(
                    fontSize: 16,
                  )),
            ],
          ),
        ),
      ],
    );
  }
}
