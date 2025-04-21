import 'package:flutter/material.dart';

class PreferencesScreen extends StatefulWidget {
  const PreferencesScreen({super.key});

  @override
  State<PreferencesScreen> createState() => _PreferencesScreenState();
}

class _PreferencesScreenState extends State<PreferencesScreen> {
  final List<String> categories = [
    "Bijoux",
    "Vêtements",
    "Décoration",
    "Accessoires",
    "Chaussures",
    "Produits locaux",
    "Beauté",
    "Électronique"
  ];

  final Set<String> selectedCategories = {};

  void toggleCategory(String category) {
    setState(() {
      if (selectedCategories.contains(category)) {
        selectedCategories.remove(category);
      } else {
        selectedCategories.add(category);
      }
    });
  }

  void validatePreferences() {
    // Tu peux enregistrer dans un backend ou localement
    print("Préférences sélectionnées : $selectedCategories");
    Navigator.pop(context); // ou push vers Store
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        gradient: RadialGradient(
          center: Alignment.center,
          radius: 0.85,
          colors: [Color(0xFF7D260F), Color(0xFF2D1B14)],
          stops: [0.08, 1.0],
        ),
      ),
      child: Scaffold(
        backgroundColor: Colors.transparent,
        appBar: AppBar(
          title: const Text("Vos préférences",
              style: TextStyle(color: Color(0xFF7D260F))),
          backgroundColor: const Color.fromRGBO(245, 230, 218, 0.5),
          foregroundColor: Colors.white,
          centerTitle: true,
        ),
        body: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "Quels types de produits aimeriez-vous voir dans votre fil ?",
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                  fontFamily: 'Playfair Display',
                ),
              ),
              const SizedBox(height: 20),
              Wrap(
                spacing: 10,
                runSpacing: 10,
                children: categories.map((category) {
                  final isSelected = selectedCategories.contains(category);
                  return FilterChip(
                    label: Text(category),
                    selected: isSelected,
                    onSelected: (_) => toggleCategory(category),
                    selectedColor: const Color(0xFF7D260F),
                    checkmarkColor: Colors.white,
                    labelStyle: TextStyle(
                      color: isSelected ? Colors.white : Colors.black87,
                      fontWeight: FontWeight.w500,
                    ),
                    backgroundColor: const Color(0xFFF5E6DA),
                  );
                }).toList(),
              ),
              const Spacer(),
              Center(
                child: ElevatedButton(
                  onPressed: selectedCategories.isNotEmpty
                      ? validatePreferences
                      : null,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF7D260F),
                    padding: const EdgeInsets.symmetric(
                        horizontal: 32, vertical: 12),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text(
                    "Valider",
                    style: TextStyle(
                      fontSize: 16,
                      color: Color(0xFFF5E6DA),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
