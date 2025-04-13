<script setup>
definePageMeta({
  layout: 'admin'
})
</script>

<template>
  <br><br><br>
  <div class="add-product-container">
    <header>
      <h2>Ajouter un produit</h2>
    </header>

    <form class="product-form">
      <div class="form-group">
        <label for="product-images">Images du produit</label>
        <input type="file" id="product-images" multiple accept="image/*" />
      </div>

      <div class="form-group">
        <label for="product-name">Nom du produit</label>
        <input type="text" id="product-name" placeholder="Nom..." />
      </div>

      <div class="form-group">
        <label for="product-category">Catégorie</label>
        <select id="product-category">
          <option value="" disabled selected>Choisir une catégorie</option>
          <option>Chez nous</option>
          <option>Accessoires</option>
          <option>Bureautique</option>
          <option>Mode</option>
          <option>Sport</option>
          <option>Art</option>
        </select>
      </div>

      <div class="form-group">
        <label for="product-description">Descriptions</label>
        <textarea id="product-description" rows="4" placeholder="Décrivez le produit..."></textarea>
      </div>

      <div class="form-group">
        <label for="product-status">État du produit</label>
        <select id="product-status">
          <option value="draft">Brouillon</option>
          <option value="published">Publié</option>
          <option value="unpublished">Non publié</option>
        </select>
      </div>

      <div class="form-buttons">
        <button type="submit" class="confirm">Confirmer</button>
        <button type="button" class="cancel">Annuler</button>
      </div>
    </form>
  </div><br><br><br>
</template>

<style scoped lang="scss">
.add-product-container {
  max-width: 700px;
  margin: 40px auto;
  padding: 40px;
  background: rgba(245, 230, 218, 0.4);
  border-radius: 20px;
  backdrop-filter: blur(6px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  font-family: 'Inter', sans-serif;

  header {
    margin-bottom: 30px;
    h2 {
      font-size: 28px;
      color: #C0A080;
      text-align: center;
    }
  }

  .product-form {
    display: flex;
    flex-direction: column;
    gap: 25px;

    .form-group {
      display: flex;
      flex-direction: column;

      label {
        font-weight: 600;
        margin-bottom: 8px;
        color: #444;
      }

      input,
      select,
      textarea {
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid #ccc;
        background: #fff;
        font-size: 16px;
        transition: border-color 0.3s ease;

        &:focus {
          outline: none;
          border-color: #C0A080;
        }
      }

      textarea {
        resize: vertical;
      }
    }

    .form-buttons {
      display: flex;
      justify-content: space-between;
      gap: 20px;

      button {
        flex: 1;
        padding: 12px 16px;
        font-size: 16px;
        border-radius: 12px;
        cursor: pointer;
        transition: background 0.3s ease, color 0.3s ease;

        &.confirm {
          background-color: #C0A080;
          color: #fff;
          border: none;

          &:hover {
            background-color: #a88966;
          }
        }

        &.cancel {
          background: transparent;
          color: #C0A080;
          border: 2px solid #C0A080;

          &:hover {
            background-color: rgba(192, 160, 128, 0.1);
          }
        }
      }
    }
  }
}
</style>
