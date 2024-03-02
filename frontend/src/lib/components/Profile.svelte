<script>
	// @ts-nocheck
	export let account;
	export let profile;
</script>

<div class="card variant-ghost-primary card-hover overflow-hidden" href="/elements/cards">
	<header>
		<img
			src={profile?.backgroundImage?.[0]?.url.replace(
				'ipfs://',
				'https://api.universalprofile.cloud/ipfs/'
			)}
			class="bg-black/50 w-full aspect-[21/9]"
			alt="bg"
		/>
	</header>
	<div class="p-4 space-y-4">
		<figure
			class="avatar flex aspect-square text-surface-50 font-semibold justify-center items-center overflow-hidden isolate bg-surface-400-500-token w-8 rounded-full"
			data-testid="avatar"
		>
			<img
				class="avatar-image w-full object-cover"
				src="https://images.unsplash.com/photo-1617296538902-887900d9b592?ixid=M3w0Njc5ODF8MHwxfGFsbHx8fHx8fHx8fDE2ODc5NzExMDB8&amp;ixlib=rb-4.0.3&amp;w=32&amp;h=32&amp;auto=format&amp;fit=crop"
				alt=""
				style=""
			/>
		</figure>
		<h6 class="h6">{account || '0x'}</h6>
		<h3 class="h3">{profile?.name || 'Anonymous'}</h3>
		<article>
			<p>Lorem ipsum dolor sit amet consectetur adipisicing elit</p>
		</article>
	</div>
	<hr class="opacity-50" />
	<footer class="p-4 flex justify-start items-center space-x-4">
		<div class="flex-auto flex justify-between items-center">
			<h6 class="font-bold" data-toc-ignore="">Amount Value</h6>
			<div>324</div>
		</div>
		<div class="flex-auto flex justify-between items-center">
			<h6 class="font-bold" data-toc-ignore="">Score</h6>
			<div>5</div>
		</div>
		<div class="flex-auto flex justify-between items-center">
			<h6 class="font-bold" data-toc-ignore="">Anoun</h6>
			<div>324</div>
		</div>
	</footer>
</div>
