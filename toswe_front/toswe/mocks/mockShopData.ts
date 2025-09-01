// /mocks/mockShopData.js
export const mockShopData = {
  shop: {
    id: 1,
    slug: "boutique-toswe",
    name: "Boutique Tôswè",
    logo_url: "/images/shop-logo.png",
    slogan: "La qualité avant tout",
    verified: true,
    about:
      "Bienvenue dans la Boutique Tôswè ! Nous proposons une sélection de produits de qualité soigneusement choisis pour répondre à vos besoins. Notre mission est de rapprocher vendeurs et clients grâce à une plateforme simple et efficace.soigneusement choisis pour répondre à vos besoins. Notre mission est de rapprocher vendeurs et clients grâce à une plateforme simple et efficace.soigneusement choisis pour répondre à vos besoins. Notre mission est de rapprocher vendeurs et clients grâce à une plateforme simple et efficace.",
    rating: 4.6,
    loyal_customers: [
      { id: 1, username: "JeanDupont", avatar: "/images/user1.jpg" },
      { id: 2, username: "AwaKoné", avatar: "/images/user2.jpg" },
      { id: 3, username: "MoussaTraore", avatar: "/images/user3.jpg" }
    ],
    owner_id: 42
  },

  ads: [
    {
      id: 101,
      title: "Promo rentrée scolaire",
      description: "Jusqu’à -30% sur les fournitures scolaires ! Offre valable jusqu’au 15 septembre.",
      image_url: "/images/ad-school.jpg"
    },
    {
      id: 102,
      title: "Nouveautés Mode",
      description: "Découvrez notre nouvelle collection avec des réductions exclusives.",
      image_url: "/images/ad-fashion.jpg"
    },
    {
      id: 103,
      title: "Promo High-Tech",
      description: "Smartphones et accessoires à prix cassés, stocks limités !",
      image_url: "/images/ad-tech.jpg"
    }
  ],

  products: [
    {
      id: 201,
      name: "Sneakers Urban",
      price: 25000,
      image_url: "/images/product-sneakers.jpg",
      rating: 4.2
    },
    {
      id: 202,
      name: "Sac à dos moderne",
      price: 18000,
      image_url: "/images/product-backpack.jpg",
      rating: 4.5
    },
    {
      id: 203,
      name: "Montre connectée",
      price: 55000,
      image_url: "/images/product-watch.jpg",
      rating: 4.8
    },
    {
      id: 204,
      name: "Chemise en lin",
      price: 15000,
      image_url: "/images/product-shirt.jpg",
      rating: 4.0
    },
    {
      id: 205,
      name: "Casque Bluetooth",
      price: 22000,
      image_url: "/images/product-headphones.jpg",
      rating: 4.7
    }
  ]
}
