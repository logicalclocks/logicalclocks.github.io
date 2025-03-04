# Hopsworks Documentation - Claude Guidance

## Build Commands
- Build and serve locally: `python -m mkdocs serve`
- Check links: `mkdocs serve & sleep 30 && linkchecker http://127.0.0.1:8000/ && kill $!`
- Install dependencies: `pip install -r requirements-docs.txt`

## Project Structure
- Documentation source in `/docs` directory
- Navigation defined in `mkdocs.yml`
- CSS customization in `/docs/css/`

## Style Guidelines
- Use Markdown for all documentation files
- Follow Material Design styling conventions
- Include descriptive alt text for all images
- Create concise, focused pages with clear headings
- Use admonitions for important notes/warnings
- Place new images in appropriate subdirectories under `/docs/assets/images/`
- Maintain consistent navigation structure in `mkdocs.yml`
- Use kebab-case for filenames (e.g., `feature-server.md`)
- Keep code examples concise and well-commented