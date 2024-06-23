<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import { LightSwitch } from '@skeletonlabs/skeleton';
	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
</script>

<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar gridColumns="grid-cols-1" slotDefault="place-self-center w-full max-w-prose" slotTrail="place-content-end">
			<!-- <svelte:fragment slot="lead">(icon)</svelte:fragment> -->
			<div class="flex space-x-4 justify-between items-center">
				<strong class="text-2xl z-10">MIDI2Arduino</strong>
				<div class='flex space-x-4 justify-center items-center'>
					<a
					class="btn btn-sm variant-ghost-surface"
					href="https://github.com/HenryMBaldwin/MIDI2Arduino"
					target="_blank"
					rel="noreferrer"
				>
					GitHub
				</a>
					<LightSwitch/>
				</div>
			</div>
			<!-- <svelte:fragment slot="trail">(actions)</svelte:fragment> -->
		</AppBar>
	</svelte:fragment>
	<!-- Page Route Content -->
	<div class="w-full ml-2 mr-4">
		<div class="size-full bg-surface-50-900-token">
			<div class='max-w-prose mx-auto flex-col items-center bg-surface-50-900-token size-full gap-10 space-y-10 py-10 '>
				<slot />
			</div>
		</div>
	</div>
</AppShell>
