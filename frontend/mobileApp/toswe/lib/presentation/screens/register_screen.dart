import 'dart:ui';
import 'package:flutter/material.dart';

class RegisterScreen extends StatelessWidget {
  const RegisterScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final nameController = TextEditingController();
    final addressController = TextEditingController();
    final phoneController = TextEditingController();
    final passwordController = TextEditingController();
    final confirmPasswordController = TextEditingController();

    return Stack(
      children: [
        // 🌄 Fond artistique
        Container(
          decoration: const BoxDecoration(
            image: DecorationImage(
              image: AssetImage("assets/toswe-africa-art.png"),
              fit: BoxFit.cover,
            ),
          ),
        ),

        // 💎 Flou artistique
        BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 8, sigmaY: 8),
          child: Container(
            color: Colors.black.withOpacity(0),
          ),
        ),

        // 🧾 Formulaire
        Scaffold(
          backgroundColor: Colors.transparent,
          appBar: AppBar(
            title: const Text("Inscription",
                style: TextStyle(color: Color(0xFF7D260F))),
            backgroundColor: const Color.fromRGBO(245, 230, 218, 0.4),
            elevation: 0,
            centerTitle: true,
          ),
          body: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  _buildTextField(
                    controller: nameController,
                    icon: Icons.person,
                    label: "Nom et prénom",
                  ),
                  const SizedBox(height: 20),
                  _buildTextField(
                    controller: addressController,
                    icon: Icons.home,
                    label: "Adresse",
                  ),
                  const SizedBox(height: 20),
                  _buildTextField(
                    controller: phoneController,
                    icon: Icons.phone,
                    label: "Numéro de téléphone",
                    keyboardType: TextInputType.phone,
                  ),
                  const SizedBox(height: 20),
                  _buildTextField(
                    controller: passwordController,
                    icon: Icons.lock,
                    label: "Mot de passe",
                    obscureText: true,
                  ),
                  const SizedBox(height: 20),
                  _buildTextField(
                    controller: confirmPasswordController,
                    icon: Icons.lock_outline,
                    label: "Confirmer le mot de passe",
                    obscureText: true,
                  ),
                  const SizedBox(height: 30),
                  ElevatedButton(
                    onPressed: () {
                      // ✍️ À compléter avec logique d'inscription
                    },
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 50, vertical: 14),
                      backgroundColor: const Color(0xFFC0A080),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12)),
                    ),
                    child: const Text(
                      "S'inscrire",
                      style: TextStyle(fontSize: 16),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextButton(
                    onPressed: () {
                      Navigator.pop(context); // Retour à la connexion
                    },
                    child: const Text(
                      "Déjà un compte ? Se connecter",
                      style: TextStyle(color: Color(0xFFC0A080)),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required IconData icon,
    required String label,
    TextInputType keyboardType = TextInputType.text,
    bool obscureText = false,
  }) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(12),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 4, sigmaY: 4),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          decoration: BoxDecoration(
            color: const Color.fromRGBO(255, 255, 255, 0.3),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.white.withOpacity(0.2)),
          ),
          child: TextField(
            controller: controller,
            keyboardType: keyboardType,
            obscureText: obscureText,
            style: const TextStyle(color: Colors.white),
            decoration: InputDecoration(
              icon: Icon(icon, color: Color(0xFFC0A080)),
              labelText: label,
              labelStyle: const TextStyle(color: Colors.white),
              border: InputBorder.none,
            ),
          ),
        ),
      ),
    );
  }
}
