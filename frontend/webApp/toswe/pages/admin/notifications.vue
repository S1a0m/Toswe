<script setup>
definePageMeta({
  layout: 'admin'
})
</script>

<template>
  <div class="home">
      <header>
      </header>
      <main>
        <TwNotificationAdmin />
        <TwNotificationAdmin />
        <TwNotificationAdmin />
        <TwNotificationAdmin />
        <TwNotificationAdmin />
      </main>
    </div>
    <button type="button">
      Nouveau
      <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#C0A080"><path d="M440-440H200v-80h240v-240h80v240h240v80H520v240h-80v-240Z"/></svg>
    </button>
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

    ul {
      list-style-type: none;
      display: flex;
      // gap: 10px;
      justify-content: space-between;
      align-items: center;
      width: 90%;

      li {
        cursor: pointer;

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
    }
  }
}

main {
  padding: 40px 80px 80px 80px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
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