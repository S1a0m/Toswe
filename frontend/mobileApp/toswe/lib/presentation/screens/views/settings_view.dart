import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:toswe/presentation/components/pop_ups/langage_popup.dart';
import 'package:toswe/presentation/components/pop_ups/preferences_popup.dart';
import 'package:toswe/presentation/components/pop_ups/edit_profil_popup.dart';
import 'package:toswe/presentation/components/pop_ups/change_password_popup.dart';

class SettingsView extends StatelessWidget {
  const SettingsView({super.key});

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

        // 💎 Flou sur l’arrière-plan
        BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 8, sigmaY: 8),
          child: Container(
            color: Colors.black.withOpacity(0), // invisible mais permet le blur
          ),
        ),

        // 📋 Contenu principal
        SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                /*const Text(
                  "Paramètres",
                  style: TextStyle(
                    color: Color(0xFF2D1B14),
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    shadows: [
                      Shadow(
                        color: Colors.white70,
                        blurRadius: 6,
                        offset: Offset(1, 2),
                      )
                    ],
                  ),
                ),*/
                const SizedBox(height: 20),
                Expanded(
                  child: ListView(
                    children: [
                      _buildSettingsItem(
                        icon: Icons.person,
                        label: "Modifier le profil",
                        onTap: () => showEditProfilePopup(context),
                      ),
                      const SizedBox(height: 10),
                      _buildSettingsItem(
                        icon: Icons.lock,
                        label: "Changer le mot de passe",
                        onTap: () => showChangePasswordPopup(context),
                      ),
                      const SizedBox(height: 10),
                      _buildSettingsItem(
                        icon: Icons.notifications,
                        label: "Notifications",
                        onTap: () {},
                      ),
                      const SizedBox(height: 10),
                      _buildSettingsItem(
                        icon: Icons.favorite,
                        label: "Préférences produits",
                        onTap: () => showPreferencesPopup(context),
                      ),
                      const SizedBox(height: 10),
                      _buildSettingsItem(
                        icon: Icons.language,
                        label: "Langue",
                        onTap: () => showLanguagePopup(context),
                      ),
                      const SizedBox(height: 10),
                      _buildSettingsItem(
                        icon: Icons.logout,
                        label: "Déconnexion",
                        onTap: () {},
                      ),
                    ],
                  ),
                )
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSettingsItem({
    required IconData icon,
    required String label,
    required VoidCallback onTap,
  }) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(12),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 4, sigmaY: 4),
        child: Container(
          decoration: BoxDecoration(
            color: const Color.fromRGBO(255, 255, 255, 0.3),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.white.withOpacity(0.2)),
          ),
          child: ListTile(
            leading: Icon(icon, color: Color(0xFFC0A080)),
            title: Text(
              label,
              style: const TextStyle(fontSize: 16, color: Color(0xFF2D1B14)),
            ),
            trailing: const Icon(Icons.arrow_forward_ios,
                size: 16, color: Colors.grey),
            onTap: onTap,
          ),
        ),
      ),
    );
  }
}
