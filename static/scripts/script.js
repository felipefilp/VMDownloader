document.addEventListener('DOMContentLoaded', () => {
    const loadingOverlay = document.getElementById('loading');

    // Função para mostrar o indicador de carregamento
    function showLoading() {
        loadingOverlay.style.display = 'flex';
    }

    // Função para esconder o indicador de carregamento
    function hideLoading() {
        loadingOverlay.style.display = 'none';
    }

    // Mostrar o carregamento ao enviar os formulários
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', (event) => {
            event.preventDefault(); // Impede o envio padrão do formulário
            showLoading();

            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json(); // Converte a resposta para JSON
            })
            .then(data => {
                // 'data' contém o URL para o download
                const link = document.createElement('a');
                link.href = data.download_url;
                link.download = ''; // O nome do arquivo será definido pelo servidor
                document.body.appendChild(link);
                link.click();
                link.remove();

                // Após o download, redireciona para a página inicial
                window.location.href = '/';
            })
            .catch(error => {
                console.error('Error:', error);
                hideLoading();
            });
        });
    });

    // Opcional: esconder o carregamento após a página carregar (se necessário)
    window.addEventListener('load', () => {
        hideLoading();
    });
});