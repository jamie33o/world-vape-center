# __World Vape Center - Portfolio Project 5__
![mockup]()

Welcome to the World Vape Center repository! This repository houses the source code for our cutting-edge vape shop website, where enthusiasts can explore and purchase a wide range of vaping products. From premium e-liquids to state-of-the-art vaping devices, World Vape Center is your go-to destination for all things vaping.

Developed by Jamie O'Neill

[Live link to website](https://world-vape-center-468f3f7d12a1.herokuapp.com/products)

## UX

When creating this site, I aimed for a straightforward design. Complicating the layout of an e-commerce store can lead to a less-than-ideal user experience, something we definitely want to avoid when encouraging users to become customers.

Throughout the site, users can easily track their basket's total while browsing and adding items. This approach builds trust with users, unlike some sites that hide this information until the checkout stage, potentially leading users to overspend.

Navigation is user-friendly through the main menu, ensuring easy exploration of all vape categories. The site is built to provide straightforward access to different vape product categories.

In essence, the site prioritizes simplicity and transparency, contributing to an overall positive and hassle-free user experience.

### Colour Scheme


- `#F7F0F5` and `#3DA5D9` used for the site background.
- `#E84610` used for primary text across the site.
- `#00bfc3` used for secondary text.
- `#ffd33b` used for highlights including headers.
- `#ff2273` used for secondary highlights such as borders around cards and the homepage button.

I used [coolors.co](https://coolors.co/383f51-bad2f2-f7f0f5-87b38d-e94f37) to generate my colour palette.

![screenshot](documentation/coolors.png)

I've used CSS `:root` variables to easily update the global colour scheme by changing only one value, instead of everywhere in the CSS file.

```css
:root {
    --magnolia: #F7F0F5;
    --charcoal: #383F51;
    --light-blue: #3DA5D9;
    --muted-green: #87B38D;
    --warn-red: #E94F37;
}
```

### Typography

When choosing fonts for the site, my main goal was to choose fonts that were easily readable for users. 

- [Caprasimo](https://fonts.google.com/specimen/Caprasimo) was used for the logo text in the main nav bar and the large text on the home page.

- [Montserrat](https://fonts.google.com/specimen/Montserrat) was used for all other text.

- [Font Awesome](https://fontawesome.com) icons were used throughout the site, such as the social media icons in the footer.
