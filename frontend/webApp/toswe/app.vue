<template>
  <div id="app">
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
  <TwDownloadApp />
  <TwAlert />
</template>

<style lang="scss">
*, body {
  margin: 0;
  padding: 0;
}


#app {
  background-image: url("/public/images/toswe-africa-art.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  // height: 100vh;
}
</style>