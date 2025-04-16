<script setup>

const formatRouteName = (routeName) => {
  const match = routeName.replace(/^admin-/, '').replace(/s$/, '').split('-')
  const firstWord = match[0] || ''
  return firstWord 
}

const router = useRouter()
const route = useRoute()

const addObject = () => {
  router.push(`/admin/${formatRouteName(route.name)}/edit?action='add'`)
}

const addNew = ref(true)

const showAddNew = () => {
  if(formatRouteName(route.name) === "user" || formatRouteName(route.name) === "message") {
    addNew.value = false
  }
  else {
    addNew.value = true
  }
}

onMounted(() => {
  showAddNew();
})

watch(() => route.name, () => {
  showAddNew()
})
</script>

<template>
  <div class="template">
    <header>
      <TwHeaderAdmin />
    </header>

    <main>
      <div class="content">
        <slot></slot>
      </div>
    </main>

    <button @click="addObject" type="button" v-if="addNew">
      Nouveau
      <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#C0A080"><path d="M440-440H200v-80h240v-240h80v240h240v80H520v240h-80v-240Z"/></svg>
    </button>
  </div>
</template>

<style lang="scss" scoped>
.content {
background-image: url("/public/images/toswe-africa-art.png");
background-repeat: no-repeat;
background-size: cover;
background-attachment: fixed;
min-height: 100vh;
}

.template {
  // height: 100vh;
  background: radial-gradient(circle, #7D260F 8%, #2D1B14 100%);
}

.basket {
position: fixed;
// background-color: #C0A080;
color: #C0A080;
background: #070707;
bottom: 50px;
right: 50px;
display: flex;
align-items: center;
justify-content: space-between;
padding: 5px;
height: 50px;
border-radius: 15px;
box-shadow: 0px 1px 4px black;
cursor: pointer;
animation: slogant 0.5s ease-out -1s infinite normal;

&:hover {
  animation: none;
}
}

@keyframes slogant {
  0%, 50% {
    transform: scale(1.10);
  }
  
  100% {
      opacity: 1;
  }
}

button {
            background: rgba(245, 230, 218, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #C0A080;
            // width: 50px;
            height: 40px;
            border: none;
            border-radius: 20px;
            border-style: solid;
            border-width: 1px;
            cursor: pointer;
            padding: 8px;
            position: fixed;
            bottom: 50px;
            right: 50px;

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
                background: rgba(245, 230, 218, 0.1);
            }
        }
</style>
