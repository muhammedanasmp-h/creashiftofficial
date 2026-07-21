const slugify = (text) => {
    return text
        .toString()
        .toLowerCase()
        .trim()
        .replace(/\s+/g, '-')           // Replace spaces with -
        .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
        .replace(/\-\-+/g, '-')         // Replace multiple - with single -
        .replace(/^-+/, '')             // Trim - from start
        .replace(/-+$/, '');            // Trim - from end
};

async function generateUniqueSlug(title, ArticleModel, excludeId = null) {
    let slug = slugify(title);
    let uniqueSlug = slug;
    let counter = 1;
    while (true) {
        const query = { slug: uniqueSlug };
        if (excludeId) {
            query._id = { $ne: excludeId };
        }
        const existing = await ArticleModel.findOne(query);
        if (!existing) {
            break;
        }
        uniqueSlug = `${slug}-${counter}`;
        counter++;
    }
    return uniqueSlug;
}

module.exports = {
    slugify,
    generateUniqueSlug
};
