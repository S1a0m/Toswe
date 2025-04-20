import 'package:flutter/material.dart';

class ProfileView extends StatelessWidget {
  const ProfileView({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          // --- Avatar ---
          const CircleAvatar(
            radius: 50,
            backgroundColor: Colors.brown,
            child: Icon(Icons.person, size: 60, color: Colors.white),
          ),
          const SizedBox(height: 12),

          // --- Statut ---
          Text(
            "Client",
            style: TextStyle(
              fontSize: 18,
              color: Colors.brown[800],
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 20),

          // --- Informations utilisateur ---
          _buildInfoRow(Icons.person, "Nom", "Jean Dupont"),
          const SizedBox(height: 12),
          _buildInfoRow(Icons.phone, "Téléphone", "+33 6 12 34 56 78"),
          const SizedBox(height: 12),
          _buildInfoRow(
              Icons.location_on, "Adresse", "12 rue des Lilas, Paris"),

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
                  color: Colors.brown,
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  // Widget helper pour chaque ligne d'info
  Widget _buildInfoRow(IconData icon, String label, String value) {
    return Row(
      children: [
        Icon(icon, color: Colors.brown),
        const SizedBox(width: 12),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label,
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 14,
                )),
            Text(value,
                style: const TextStyle(
                  fontSize: 16,
                )),
          ],
        )
      ],
    );
  }
}
