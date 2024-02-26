<script lang="ts">
    import '$src/styles.pcss';
    import ErrorMessageView from '$lib/components/ErrorMessageView.svelte';
    export let data;
</script>

<div class="app content-grid">
    <header class="full-width content-grid">
        <Header />
        <ErrorMessageView />
    </header>
    <main class="full-width content-grid">
        <slot />
    </main>
    <footer class="full-width content-grid">
        <Footer />
    </footer>
</div>


<style lang="postcss">
    .app {
        min-height: 100vh;
        min-height: 100svh;
        display: grid;
        grid-template-rows: auto 1fr auto;
    }
    header {
        grid-template-rows: var(--header-height) auto;
        background-color: theme('colors.primary.300');
    }
    main {
        height: 100%;
        width: 100%;
        background-color: theme('colors.primary.100');
    }
    footer {
        background-color: theme('colors.primary.300');
    }
</style>
