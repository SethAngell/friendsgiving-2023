const state = {
  menu: {},
  dev: false,
  current_item: 1,
};

const CONSTANTS = {
  dev_menu_endpoint: "http://localhost:8012/api/menu",
  prod_menu_endpoint: "https://friendsgiving.doublel.studio/api/menu",
  menu_categories: {
    Entree: "entree-list",
    Appetizer: "appetizer-list",
    Side: "side-list",
    Dessert: "dessert-list",
    Drink: "drink-list",
  },
};

const templates = {
  food_template: "<li>{ITEM_NAME} prepared by {CHEF_NAME}</li>",
  drink_template: "<li>{ITEM_NAME} provided by {CHEF_NAME}</li>",
};

const option_partial = `<div class="new-item-instance">
  <label for="new-item-{INDEX}">New Item {INDEX}</label>
  <div class="new-item-container">
    <select id="new-item-type-{INDEX}" name="new-item-type-{INDEX}">
      <option value="appetizer">Appetizer</option>
      <option value="entree">Entree</option>
      <option value="side">Side</option>
      <option value="dessert">Dessert</option>
      <option value="drink">Drink</option>
    </select>
    <input type="text" name="new-item-{INDEX}" id="new-item={INDEX}" />
  </div>
</div>`;

async function get_menu() {
  menu_url = state.dev ? CONSTANTS.dev_menu_endpoint : CONSTANTS.prod_menu_endpoint;
  return fetch(menu_url);
}

function add_food_to_menu() {
  Object.keys(CONSTANTS.menu_categories).forEach((category) => {
    const menu_element = document.getElementById(
      CONSTANTS.menu_categories[category]
    );

    const items = state.menu.filter(
      (element) =>
        element.type.toLocaleLowerCase() == category.toLocaleLowerCase()
    );

    if (items && items?.length > 0) {
      
      items.forEach((item) => {
        template =
          item.type.toLocaleLowerCase() == "drink"
            ? templates.drink_template
            : templates.food_template;
        menu_element.innerHTML += template
          .replace("{ITEM_NAME}", item.item)
          .replace("{CHEF_NAME}", item.chef.name);
      });
    }
  });
}

function add_drinks_to_menu() {
  Object.keys(CONSTANTS.drink_categories).forEach((category) => {
    const menu_element = document.getElementById(
      CONSTANTS.drink_categories[category]
    );

    const items = state.menu.filter(
      (element) =>
        element.type.toLocaleLowerCase() == category.toLocaleLowerCase()
    );

    if (!items || items?.length < 1) {
      menu_element.innerHTML += "<li>That is too be seen...</li>";
    } else {
      items.forEach((item) => {
        menu_element.innerHTML += templates.drink_template
          .replace("{ITEM_NAME}", item.item)
          .replace("{CHEF_NAME}", item.chef.name);
      });
    }
  });
}

function add_new_item() {
  const guest_item_container = document.getElementById("guest-items");
  guest_item_container.innerHTML += option_partial.replaceAll(
    "{INDEX}",
    state.current_item++
  );
}

get_menu()
  .then((response) => response.json())
  .then((data) => {
    state.menu = data.items;
  })
  .then(() => {
    add_food_to_menu();
  });

console.log('Oh hey there. I\'m guessing this is either Cody or Trace reading this. hows it going my guys? El Cerro or Big Thai this week?')
