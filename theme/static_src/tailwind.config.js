/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                links: " #f7f3ea", // Custom blue
                linksHover: " #F9FAFB", // Custom blue
                mainBackground: " #F9FAFB", // Custom gray
                footer: " #1A202C", // Custom gray

                button: " #2c3e50", 
                buttonHover: " #5584b0 ", 
                buttonText: " #f7f3ea", // Custom white
                buttonTextHover: "rgb(4, 24, 91)", // Custom white

              },
              backgroundImage: {
                'button1': "radial-gradient(180deg, #f7f3ea 0%, #5584b0 100%)",
                'header': "linear-gradient(180deg, #2c3e50, #254e7a)",
                'secondaryBackground': "radial-gradient(circle, #5584b0  100%, #2c3e50 0%)",
                'button': "linear-gradient(0deg, #254e7a, #82c2e6)",
                'buttonHover': "radial-gradient(circle, #5584b0, #cbe3ef)",
              },
              fontFamily: {
                poppins: ["Poppins", "sans-serif"],
                roboto: ["Roboto", "sans-serif"],
                montserrat: ["Montserrat", "sans-serif"],
                linksFont: ["Fjalla One", "sans-serif"]
              },
        },
        keyframes: {
            underlineGrow: {
              "0%": { width: "0%" },
              "100%": { width: "100%" },
            },
          },
          animation: {
            "underline-grow": "underlineGrow 0.3s ease-in-out forwards",
          },
    },
    safelist: [
        "bg-button",
        "hover:bg-buttonHover",
        "text-header",
        "text-links",
        "hover:text-linksHover",
        "bg-mainBackground",
        "bg-secondaryBackground",
        "bg-footer",
        "max-h-[500px]", 
        "opacity-100"
    ],
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
