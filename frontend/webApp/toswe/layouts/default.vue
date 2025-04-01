<template>
    <div class="template">
      <header>
        <TwHeader />
      </header>
  
      <main>
        <slot></slot>
        <div class="basket">
          00
          <svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="30px" fill="#2D1B14"><path d="M221-120q-27 0-48-16.5T144-179L42-549q-5-19 6.5-35T80-600h190l176-262q5-8 14-13t19-5q10 0 19 5t14 13l176 262h192q20 0 31.5 16t6.5 35L816-179q-8 26-29 42.5T739-120H221Zm-1-80h520l88-320H132l88 320Zm260-80q33 0 56.5-23.5T560-360q0-33-23.5-56.5T480-440q-33 0-56.5 23.5T400-360q0 33 23.5 56.5T480-280ZM367-600h225L479-768 367-600Zm113 240Z"/></svg>
        </div>
      </main>
  
      <footer>
        <TwFooter />
      </footer>
    </div>
</template>
  
<style lang="scss" scoped>
$page-background: #2D1B14;

.template {
    height: 100vh;
    background: radial-gradient(circle, #7D260F 8%, #2D1B14 100%);
}

.basket {
  position: fixed;
  background-color: #C0A080;
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
}
</style>
  