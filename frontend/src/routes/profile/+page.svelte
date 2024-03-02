<script>
	// @ts-nocheck

	import Profile from '$lib/components/Profile.svelte';
	import { accountStore } from '$lib/stores';
	import { luksoStore } from '$lib/stores';

	let accounts = [];
	let profile = null;

	accountStore.subscribe((value) => {
		accounts = value;
	});
	luksoStore.subscribe((value) => {
		profile = value;
	});
</script>

<div class="stack grid place-items-center mt-40">
	<Profile account={accounts[0]} profile={profile.value?.LSP3Profile} />
</div>
