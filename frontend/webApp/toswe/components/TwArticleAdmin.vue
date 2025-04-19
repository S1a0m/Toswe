<script setup>
const props = defineProps([
    "id",
    "img",
    "name",
    "price",
    "status",
])

async function onDelete() {
  const token = localStorage.getItem("access_token")

  try {
    const response = await fetch(`http://localhost:8000/admin/products/${props.id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      throw new Error("Erreur lors de la suppression.")
    }

    emit('deleted', props.id) // <== ici tu préviens le parent

  } catch (error) {
    console.error(error)
    alert("Échec lors de la suppression.")
  }
}


const img = ref(`http://127.0.0.1:8000/${props.img}`)

watch(() => props.img, () => {
    img.value = `http://127.0.0.1:8000/${props.img}`
})
</script>


<template>
    <article>
        <span :class="['status-dot', props.status]"></span>
        <img :src="img" alt="">
        <div>
            <h3>{{ props.name }}</h3> ···
            <p>{{ props.price }} fcfa</p>
        </div>
        <div>
            <NuxtLink :to="{name: 'admin-product-read', query: {id: props.id}}">
                <button type="button">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#C0A080"><path d="M440-440H200v-80h240v-240h80v240h240v80H520v240h-80v-240Z"/></svg>
                </button>
            </NuxtLink>
            <NuxtLink :to="{name: 'admin-product-edit', query: {id: props.id}}">
                <button type="button">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#C0A080"><path d="M200-200h57l391-391-57-57-391 391v57Zm-80 80v-170l528-527q12-11 26.5-17t30.5-6q16 0 31 6t26 18l55 56q12 11 17.5 26t5.5 30q0 16-5.5 30.5T817-647L290-120H120Zm640-584-56-56 56 56Zm-141 85-28-29 57 57-29-28Z"/></svg>
                </button>
            </NuxtLink>
            <button type="button" @click="onDelete">
                <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#C0A080"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/></svg>
            </button>
        </div>
    </article>
</template>

<style lang="scss" scoped>
article {
    position: relative;
    background: rgba(245, 230, 218, 0.7);
    width: 325px;
    height: 420px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    backdrop-filter: blur(4px);
    transition: all 0.45s 0s ease;

    &:hover {
        transform: translateY(-10px);
        box-shadow: 0px 1px 4px black;
    }

    img {
        width: 280px;
        height: 280px;
        border-radius: 10px;
        cursor: pointer;
    }

    div {
        display: flex;
        align-items: center;
        // justify-content: space-between;
        gap: 20px;
        color: #7D260F;
        margin: 15px 0px 0px 0px ;
        h3 {
            font: {
                family: "Lora";
            }   
        }

        p {
            font: {
                family: "Lora";
                weight: 600;
            } 
        }
    }

    div {
        button {
            background: rgba(245, 230, 218, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #C0A080;
            width: 50px;
            height: 40px;
            border: none;
            border-radius: 20px;
            border-style: solid;
            border-width: 1px;
            cursor: pointer;

            font: {
                size: 16px;
                weight: bold;
                family: "Inter"
            }
            /*width: 50px;
            height: 50px;
            border-radius: 50%;*/

            &:hover {
                box-shadow: 0px 1px 4px black;
            }
        }
    }
}

.more {
    font: {
        size: 12px;
    }
}

.status-dot {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid white;
  z-index: 10;
}

/* Couleurs selon le statut */
.status-dot.published {
  background-color: #16a34a; // vert
}
.status-dot.unpublished {
  background-color: #dc2626; // rouge
}
.status-dot.draft {
  background-color: #6b7280; // gris
}

</style>