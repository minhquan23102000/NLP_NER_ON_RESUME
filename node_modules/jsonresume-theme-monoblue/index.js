const fs = require('fs');
const path = require('path');
const Handlebars = require('handlebars');
const sass = require('sass');

const SRC = `${__dirname}/src`;

Handlebars.registerHelper('ifwith', function(context, options) {
  if (context && Object.keys(context).length) {
    return options.fn(context);
  }
});

Handlebars.registerHelper('fa-convert', function(string) {
  return string.replace(/\s/g, '-').toLowerCase()
});

function render(resume) {
  const css = sass.compile(`${SRC}/styles/main.scss`).css;
  const tpl = fs.readFileSync(`${SRC}/templates/index.hbs`, 'utf-8');
  const partialsDir = `${SRC}/templates/partials`;
  const filenames = fs.readdirSync(partialsDir);

  filenames.forEach(filename => {
    const parsedPath = path.parse(filename);

    if (parsedPath.ext === '.hbs') {
      const filepath = path.join(partialsDir, filename);
      const template = fs.readFileSync(filepath, 'utf-8');

      Handlebars.registerPartial(parsedPath.name, template);
    }
  });

  return Handlebars.compile(tpl)({
    css,
    resume
  });
}

module.exports = {
  render: render
};