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
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // --- Menu horizontal des catégories avec icône fixe ---
        Row(
          children: [
            const Padding(
              padding: EdgeInsets.only(right: 8.0),
              child: Icon(Icons.shopping_cart_outlined, color: Colors.brown),
            ),
            Expanded(
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: categories.map((category) {
                    final isSelected = selectedCategory == category;
                    return Padding(
                      padding: const EdgeInsets.only(right: 8.0),
                      child: ChoiceChip(
                        label: Text(category),
                        selected: isSelected,
                        onSelected: (_) {
                          setState(() {
                            selectedCategory = category;
                            // filtrer produits
                          });
                        },
                        selectedColor: Colors.brown[200],
                        backgroundColor: Colors.brown[50],
                        labelStyle: TextStyle(
                          color: isSelected ? Colors.white : Colors.brown[800],
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ),
            ),
          ],
        ),

        const SizedBox(height: 20),

        // --- GridView des produits ---
        GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            crossAxisSpacing: 12,
            mainAxisSpacing: 12,
            childAspectRatio: 0.82, // toujours important
          ),
          itemCount: 10,
          itemBuilder: (context, index) => const ProductCart(),
        ),
      ],
    );
  }
}
