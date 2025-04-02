<template>
  <div class="about-content">
    <section>
      <h2>· Nous ecrire via WhatsApp ·</h2>
      <div class="whatsapp inputs">
        <textarea name="" id="" placeholder="Ecrivez votre message whatsapp ici..."></textarea>
        <button type="submit">
          Envoyer
          <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#2D1B14"><path d="M120-160v-640l760 320-760 320Zm80-120 474-200-474-200v140l240 60-240 60v140Zm0 0v-400 400Z"/></svg>
        </button>
      </div>
    </section><br><br><br>
    <section>
      <h2>· Nous envoyer un mail ·</h2>
      <div class="mail inputs">
        <textarea name="" id="" placeholder="Ecrivez votre mail ici..."></textarea>
        <input type="text" name="" id="" placeholder="Mentionnez votre nom...">
        <button type="submit">
          Envoyer
          <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#2D1B14"><path d="M120-160v-640l760 320-760 320Zm80-120 474-200-474-200v140l240 60-240 60v140Zm0 0v-400 400Z"/></svg>
        </button>
      </div>
    </section><br><br><br>
  </div>
</template>
  

<style lang="scss" scoped>
.about-content {
  padding: 40px 80px 80px 80px;
}

section {
  h2 {
    color: #EFE8E8;
  }

  .inputs {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: flex-start;
    gap: 20px;

    textarea {
      height: 231px;
      width: 1192px;
      background: rgba(239, 232, 232, 0.8);
      padding: 2em;

      font: {
        size: 16px;
      }
    }

    input {
      // height: 50px;
      width: 1192px;
      background: rgba(239, 232, 232, 0.8);
      padding: 2em;

      font: {
        size: 16px;
      }
    }

    button {
      display: flex;
      justify-content: center;
      align-items: center;
      color: #2D1B14;
      width: 135px;
      height: 63px;
      border-radius: 20px;
      background: #EFE8E8;
      border-style: none;

      font: {
        size: 18px;
        weight: bold;
      }
    }
  }
}

</style>