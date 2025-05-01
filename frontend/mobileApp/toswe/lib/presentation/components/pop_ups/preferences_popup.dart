import 'dart:ui';
import 'package:flutter/material.dart';

Future<void> showPreferencesPopup(BuildContext context) async {
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

  await showDialog(
    context: context,
    barrierDismissible: true,
    builder: (BuildContext context) {
      return Dialog(
        backgroundColor: Colors.transparent,
        insetPadding: const EdgeInsets.all(20),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
          child: Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: const Color.fromRGBO(245, 230, 218, 0.85),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: Colors.white.withOpacity(0.3)),
            ),
            child: StatefulBuilder(
              builder: (context, setState) {
                return Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Text(
                      "Préférences produits",
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF7D260F),
                        fontFamily: 'Playfair Display',
                      ),
                    ),
                    const SizedBox(height: 10),
                    const Text(
                      "Quels types de produits aimeriez-vous voir ?",
                      style: TextStyle(
                        fontSize: 16,
                        color: Color(0xFF2D1B14),
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 20),
                    Wrap(
                      spacing: 10,
                      runSpacing: 10,
                      children: categories.map((category) {
                        final isSelected =
                            selectedCategories.contains(category);
                        return FilterChip(
                          label: Text(category),
                          selected: isSelected,
                          onSelected: (_) {
                            setState(() {
                              if (isSelected) {
                                selectedCategories.remove(category);
                              } else {
                                selectedCategories.add(category);
                              }
                            });
                          },
                          selectedColor: const Color(0xFF7D260F),
                          checkmarkColor: Colors.white,
                          labelStyle: TextStyle(
                            color: isSelected
                                ? Colors.white
                                : const Color(0xFF2D1B14),
                            fontWeight: FontWeight.w500,
                          ),
                          backgroundColor: const Color(0xFFF5E6DA),
                        );
                      }).toList(),
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: selectedCategories.isNotEmpty
                          ? () {
                              print("Préférences : $selectedCategories");
                              Navigator.of(context).pop();
                            }
                          : null,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF7D260F),
                        disabledBackgroundColor: Colors.grey.shade400,
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
                    )
                  ],
                );
              },
            ),
          ),
        ),
      );
    },
  );
}
