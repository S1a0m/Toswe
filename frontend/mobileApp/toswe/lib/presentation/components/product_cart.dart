import 'package:flutter/material.dart';
import 'package:toswe/presentation/screens/product_detail_screen.dart';

class ProductCart extends StatelessWidget {
  final String imagePath;
  final String productName;
  final String price;

  const ProductCart({
    super.key,
    required this.imagePath,
    required this.productName,
    required this.price,
  });

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
            // ✅ Image du produit
            Center(
              child: ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.asset(
                  imagePath,
                  width: 150,
                  height: 150,
                  fit: BoxFit.cover,
                ),
              ),
            ),
            const SizedBox(height: 12),
            Text(
              productName,
              style: const TextStyle(
                fontFamily: 'Playfair Display',
                fontWeight: FontWeight.w600,
                fontSize: 16,
                color: Color(0xFF2D1B14),
              ),
            ),
            const SizedBox(height: 6),
            Text(
              price,
              style: const TextStyle(
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
              Navigator.push(context, MaterialPageRoute(builder: (context) {
                return ProductDetailScreen();
              }));
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
