import 'package:flutter/material.dart';
import 'package:toswe/presentation/screens/register_screen.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final phoneController = TextEditingController();
    final passwordController = TextEditingController();

    return Container(
      decoration: const BoxDecoration(
        gradient: RadialGradient(
          center: Alignment.center,
          radius: 0.85,
          colors: [
            Color(0xFF7D260F),
            Color(0xFF2D1B14),
          ],
          stops: [0.08, 1.0],
        ),
      ),
      child: Scaffold(
        backgroundColor: Colors.transparent,
        appBar: AppBar(
          backgroundColor: const Color.fromRGBO(245, 230, 218, 0.5),
          elevation: 18.0,
          leadingWidth: 300,
          leading: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Image.asset('assets/logo-toswe.png', width: 32, height: 32),
                const SizedBox(width: 8),
                const Text(
                  "Tôswè - Connexion",
                  style: TextStyle(
                    fontFamily: 'Playfair Display',
                    fontWeight: FontWeight.w600,
                    fontSize: 20,
                    color: Color(0xFF7D260F),
                  ),
                ),
              ],
            ),
          ),
        ),
        body: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              TextField(
                controller: phoneController,
                keyboardType: TextInputType.phone,
                decoration:
                    const InputDecoration(labelText: "Numéro de téléphone"),
              ),
              TextField(
                controller: passwordController,
                obscureText: true,
                decoration: const InputDecoration(labelText: "Mot de passe"),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                  onPressed: () {}, child: const Text("Se connecter")),
              TextButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const RegisterScreen()),
                  );
                },
                child: const Text("Pas encore inscrit ? S'inscrire"),
              )
            ],
          ),
        ),
      ),
    );
  }
}
