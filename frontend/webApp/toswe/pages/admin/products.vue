<script setup>
definePageMeta({
  layout: 'admin'
})

const articles = ref([]);
const activeCategory = ref('');

const categories = [
  { name: "Tout", value: "all" },
  { name: "Chez nous", value: "local" },
  { name: "Accessoires", value: "accessories" },
  { name: "Bureautique", value: "computer" },
  { name: "Mode", value: "fashion" },
  { name: "Sport", value: "sport" },
  { name: "Art", value: "art" },
];

async function fetchArticleByCategory(category) {
  activeCategory.value = category;
  const token = localStorage.getItem("access_token")

  try {
    const response = await fetch(`http://localhost:8000/admin/products/?category=${category}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error("Erreur lors de la réception.")
    }

    const data = await response.json();
    articles.value = data;

  } catch (error) {
    console.error(error)
    alert("Échec lors de la réception.")
  }
}

function removeProduct(id) {
  articles.value = articles.value.filter(article => article.id !== id)
}

onMounted(() => {
  fetchArticleByCategory('all')
})

</script>

<template>
  <div class="home">
      <header>
        <div class="shopping-cart">
          <svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#C0A080"><path d="M280-80q-33 0-56.5-23.5T200-160q0-33 23.5-56.5T280-240q33 0 56.5 23.5T360-160q0 33-23.5 56.5T280-80Zm400 0q-33 0-56.5-23.5T600-160q0-33 23.5-56.5T680-240q33 0 56.5 23.5T760-160q0 33-23.5 56.5T680-80ZM246-720l96 200h280l110-200H246Zm-38-80h590q23 0 35 20.5t1 41.5L692-482q-11 20-29.5 31T622-440H324l-44 80h480v80H280q-45 0-68-39.5t-2-78.5l54-98-144-304H40v-80h130l38 80Zm134 280h280-280Z"/></svg>
          <!--<svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#C0A080"><path d="M284.53-80.67q-30.86 0-52.7-21.97Q210-124.62 210-155.47q0-30.86 21.98-52.7Q253.95-230 284.81-230t52.69 21.98q21.83 21.97 21.83 52.83t-21.97 52.69q-21.98 21.83-52.83 21.83Zm400 0q-30.86 0-52.7-21.97Q610-124.62 610-155.47q0-30.86 21.98-52.7Q653.95-230 684.81-230t52.69 21.98q21.83 21.97 21.83 52.83t-21.97 52.69q-21.98 21.83-52.83 21.83ZM206-800.67h589.38q22.98 0 34.97 20.84 11.98 20.83.32 41.83L693.33-490.67q-11 19.34-28.87 30.67-17.87 11.33-39.13 11.33H324l-52 96h487.33V-286H278q-43 0-63-31.83-20-31.84-.33-68.17l60.66-111.33-149.33-316H47.33V-880h121.34L206-800.67Z"/></svg>-->
          :
        </div>
        <nav>
          <ul>
            <li 
              v-for="cat in categories" 
              :key="cat.value" 
              @click="fetchArticleByCategory(cat.value)"
              :class="{ active: activeCategory === cat.value }"
            >
              {{ cat.name }}
            </li>
          </ul>
        </nav>
      </header>
      <main>
        <TwArticleAdmin v-for="article in articles" v-bind="article" :key="article.id" :id="article.id_product" :img="article.image" :name="article.name" :price="article.price" :status="article.status" @deleted="removeProduct"/>
      </main>
    </div>
</template>

<style lang="scss" scoped>


header {
  display: flex;
  padding: 30px;
  align-items: center;
  justify-content: space-between;

  .shopping-cart {
    background: rgba(245, 230, 218, 0.3);
    width: 72px;
    height: 50px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(4px);
    color: #C0A080;

    font: {
      weight: bold;
      size: 18px;
    }
  }

  nav {
    background: rgba(245, 230, 218, 0.3);
    width: 92vw;
    height: 50px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(4px);

    /*ul {
      list-style-type: none;
      display: flex;
      // gap: 10px;
      justify-content: space-between;
      align-items: center;
      width: 90%;

      li {
        cursor: pointer;
        transition: all 0.3s ease;
        font: {
            // size: 20px;
            // weight: 500;
            family: "Lora";
        }

        &:hover {
          color: #C0A080;
          text-decoration: underline;
          text-decoration-thickness: 2px;
          text-underline-offset: 8px;
        }
      }

      .active-categorie-page {
        color: #C0A080;
        text-decoration: underline;
        text-decoration-thickness: 2px;
        text-underline-offset: 8px;
      }
    }*/
  }
}

nav ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

nav ul li {
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: "Lora";
  padding: 8px 12px;
  border-radius: 4px;
  background-color: transparent;
  color: #2D1B14;
  border: 1px solid transparent;
}

nav ul li:hover {
  background-color: #f5e6da;
}

nav ul li.active {
  background-color: #C0A080;
  color: white;
  font-weight: bold;
}

main {
  padding: 40px 80px 80px 80px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}
</style>