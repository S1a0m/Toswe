import 'dart:ui';
import 'package:flutter/material.dart';

Future<void> showLanguagePopup(BuildContext context) async {
  String selectedLanguage = 'Français';

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
                      "Choix de la langue",
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF7D260F),
                        fontFamily: 'Playfair Display',
                      ),
                    ),
                    const SizedBox(height: 20),
                    RadioListTile<String>(
                      title: const Text('Français'),
                      value: 'Français',
                      groupValue: selectedLanguage,
                      onChanged: (value) {
                        setState(() => selectedLanguage = value!);
                      },
                    ),
                    RadioListTile<String>(
                      title: const Text('Anglais'),
                      value: 'Anglais',
                      groupValue: selectedLanguage,
                      onChanged: (value) {
                        setState(() => selectedLanguage = value!);
                      },
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: () {
                        print("Langue sélectionnée : \$selectedLanguage");
                        Navigator.of(context).pop();
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF7D260F),
                        padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 12),
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
