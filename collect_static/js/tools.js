// tools.js

document.addEventListener('DOMContentLoaded', function () {
    const toolsBtn = document.getElementById('tools-btn');
    const toolsMenu = document.getElementById('tools-menu');

    // 点击 Tools 按钮显示/隐藏子菜单
    toolsBtn.addEventListener('click', function () {
        const expanded = toolsBtn.getAttribute('aria-expanded') === 'true' || false;
        toolsBtn.setAttribute('aria-expanded', !expanded);
        toolsMenu.classList.toggle('hidden');
    });

    // 点击其他地方隐藏子菜单
    document.addEventListener('click', function (event) {
        if (!toolsMenu.contains(event.target) && event.target !== toolsBtn) {
            toolsBtn.setAttribute('aria-expanded', 'false');
            toolsMenu.classList.add('hidden');
        }
    });
});
