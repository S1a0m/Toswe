import 'package:flutter/material.dart';

class ProductCart extends StatelessWidget {
  const ProductCart({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: const Color.fromRGBO(245, 230, 218, 0.8),
        borderRadius: BorderRadius.circular(16),
        boxShadow: const [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 6,
            offset: Offset(2, 4),
          )
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Center(
              child: Icon(
                Icons.shopping_bag,
                size: 48,
                color: Color(0xFF7D260F),
              ),
            ),
            const SizedBox(height: 12),
            const Text(
              "Produit Exquis",
              style: TextStyle(
                fontFamily: 'Playfair Display',
                fontWeight: FontWeight.w600,
                fontSize: 16,
                color: Color(0xFF2D1B14),
              ),
            ),
            const SizedBox(height: 6),
            const Text(
              "2500 fcfa",
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.bold,
                color: Color(0xFF7D260F),
              ),
            ),
            const SizedBox(height: 8),
            Align(
              alignment: Alignment.centerRight,
              child: ElevatedButton(
                onPressed: () {
                  // Ajouter au panier
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF7D260F),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  padding: const EdgeInsets.all(8),
                  elevation: 4,
                ),
                child: const Icon(
                  Icons.add_shopping_cart,
                  size: 20,
                  color: Color(0xFFF5E6DA),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
