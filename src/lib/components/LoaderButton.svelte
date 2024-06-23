<script lang="ts">
    import Loader from '$lib/components/Loader.svelte';
    
    export let loading: boolean = false;
    export let btnClass: string = '';
    export let btnId: string = '';
    export let onClick = () => {};
    export let text: string = '';
    
    </script>
    
    {#if !loading}
        <button class={btnClass} on:click={onClick} id={btnId}>{text}</button>
    {:else}
        <Loader />
    {/if}
            