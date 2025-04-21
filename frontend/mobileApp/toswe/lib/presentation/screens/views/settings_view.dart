import 'package:flutter/material.dart';
import 'package:toswe/presentation/screens/preferences_screen.dart';

class SettingsView extends StatelessWidget {
  const SettingsView({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "Paramètres",
            style: TextStyle(
              color: Colors.brown,
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 20),
          _buildSettingsItem(
            icon: Icons.person,
            label: "Modifier le profil",
            onTap: () {
              // Naviguer vers la modification du profil
            },
          ),
          const Divider(),
          _buildSettingsItem(
            icon: Icons.lock,
            label: "Changer le mot de passe",
            onTap: () {
              // Action mot de passe
            },
          ),
          const Divider(),
          _buildSettingsItem(
            icon: Icons.notifications,
            label: "Notifications",
            onTap: () {
              // Action notifications
            },
          ),
          const Divider(),
          _buildSettingsItem(
            icon: Icons.favorite,
            label: "Préférences produits",
            onTap: () {
              Navigator.push(context, MaterialPageRoute(builder: (context) {
                return PreferencesScreen();
              }));
            },
          ),
          const Divider(),
          _buildSettingsItem(
            icon: Icons.language,
            label: "Langue",
            onTap: () {
              // Action langue
            },
          ),
          const Divider(),
          _buildSettingsItem(
            icon: Icons.logout,
            label: "Déconnexion",
            onTap: () {
              // Action déconnexion
            },
          ),
        ],
      ),
    );
  }

  Widget _buildSettingsItem({
    required IconData icon,
    required String label,
    required VoidCallback onTap,
  }) {
    return ListTile(
      leading: Icon(icon, color: Colors.brown),
      title: Text(label, style: const TextStyle(fontSize: 16)),
      trailing:
          const Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey),
      onTap: onTap,
    );
  }
}
