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

    <footer>
      <TwFooter />
    </footer>
  </div>
</template>

<style lang="scss" scoped>
.content {
background-image: url("/public/images/toswe-africa-art.png");
background-repeat: no-repeat;
background-size: cover;
background-attachment: fixed;
// height: 100vh;
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
</style>
