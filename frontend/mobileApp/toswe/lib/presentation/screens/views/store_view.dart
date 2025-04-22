import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:toswe/presentation/components/product_cart.dart';

class StoreView extends StatefulWidget {
  const StoreView({super.key});

  @override
  State<StoreView> createState() => _StoreViewState();
}

class _StoreViewState extends State<StoreView> {
  final List<String> categories = [
    "Tous",
    "Électronique",
    "Vêtements",
    "Maison",
    "Livres",
    "Beauté",
    "Sport",
  ];

  String selectedCategory = "Tous";

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        image: DecorationImage(
          image: AssetImage("assets/toswe-africa-art.png"),
          fit: BoxFit.cover,
        ),
      ),
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // --- MENU DES CATÉGORIES (avec blur glassmorphism) ---
          ClipRRect(
            borderRadius: BorderRadius.circular(12),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
              child: Container(
                padding:
                    const EdgeInsets.symmetric(vertical: 10, horizontal: 12),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.white.withOpacity(0.2)),
                ),
                child: Row(
                  children: [
                    Container(
                      height: 40,
                      width: 50,
                      decoration: BoxDecoration(
                        color: const Color.fromRGBO(245, 230, 218, 0.7),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: const Icon(Icons.shopping_cart,
                          color: Color(0xFF2D1B14)),
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: Row(
                          children: categories.map((category) {
                            final isSelected = selectedCategory == category;
                            return Padding(
                              padding: const EdgeInsets.only(right: 8),
                              child: ChoiceChip(
                                label: Text(category),
                                selected: isSelected,
                                onSelected: (_) {
                                  setState(() => selectedCategory = category);
                                },
                                selectedColor: const Color(0xFFC0A080),
                                backgroundColor:
                                    Colors.brown[50]?.withOpacity(0.5),
                                labelStyle: TextStyle(
                                  color: isSelected
                                      ? Colors.white
                                      : Colors.brown[800],
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            );
                          }).toList(),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),

          const SizedBox(height: 20),

          // --- PRODUITS (chaque produit sur un fond doux) ---
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              childAspectRatio: 0.55,
            ),
            itemCount: 10,
            itemBuilder: (context, index) => Container(
              decoration: BoxDecoration(
                //color: Colors.white.withOpacity(0.8),
                borderRadius: BorderRadius.circular(12),
                boxShadow: [
                  BoxShadow(
                    color: Colors.brown.withOpacity(0.15),
                    blurRadius: 6,
                    offset: const Offset(2, 4),
                  ),
                ],
              ),
              child: const ProductCart(
                imagePath: 'assets/images/bijou.jpeg',
                productName: 'Bracelet Africain',
                price: '2500 FCFA',
              ),
            ),
          ),
        ],
      ),
    );
  }
}
