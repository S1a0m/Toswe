<template>
    <div class="home">
      <header>
        <div class="shopping-cart">
          <svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#C0A080"><path d="M280-80q-33 0-56.5-23.5T200-160q0-33 23.5-56.5T280-240q33 0 56.5 23.5T360-160q0 33-23.5 56.5T280-80Zm400 0q-33 0-56.5-23.5T600-160q0-33 23.5-56.5T680-240q33 0 56.5 23.5T760-160q0 33-23.5 56.5T680-80ZM246-720l96 200h280l110-200H246Zm-38-80h590q23 0 35 20.5t1 41.5L692-482q-11 20-29.5 31T622-440H324l-44 80h480v80H280q-45 0-68-39.5t-2-78.5l54-98-144-304H40v-80h130l38 80Zm134 280h280-280Z"/></svg>
          :
        </div>
        <nav>
          <ul>
            <li class="active-categorie-page"><TwCategoriePageLink>Selectionner pour vous</TwCategoriePageLink></li>
            <li><TwCategoriePageLink>Chez nous</TwCategoriePageLink></li>
            <li><TwCategoriePageLink>Accessoires</TwCategoriePageLink></li>
            <li><TwCategoriePageLink>Bureautique</TwCategoriePageLink></li>
            <li><TwCategoriePageLink>Mode</TwCategoriePageLink></li>
            <li><TwCategoriePageLink>Sport</TwCategoriePageLink></li>
            <li><TwCategoriePageLink>Art</TwCategoriePageLink></li>
          </ul>
        </nav>
      </header>
      <main>
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
        <TwArticle />
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
</style>