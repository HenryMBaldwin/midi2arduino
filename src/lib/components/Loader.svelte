<script>
    export let size = '30px'; // Default size if not provided
</script>

<div class="flex justify-center items-center">
    <div 
        class="loader border-4 border-gray-200 border-t-primary-500 rounded-full animate-spin"
        style="width: {size}; height: {size}; border-width: {parseInt(size) / 7}px;">
    </div>
</div>

<style>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .loader {
        animation: spin 2s linear infinite;
    }
</style>