<script>
    // @ts-nocheck
	import {APP_MODE} from '$lib/consts';
	import {mode} from '$lib/stores'

	let modeSlectOpen = false;
    let selectedMode = APP_MODE.NORMAL;

	function toggleMode() {
		modeSlectOpen = !modeSlectOpen;
	}
	function selectMode(selectedMdoe) {
		mode.set(selectedMdoe)
        modeSlectOpen = false
	}
    mode.set(APP_MODE.NORMAL)

    mode.subscribe((value) => {
        selectedMode = value
    })
// TODO: add mode descriptions
</script>

<div>
    <div class="mr-24 select" on:click={toggleMode}>{selectedMode}</div>
    {#if modeSlectOpen}
        <dl class="list-dl select-list bg-surface-100-800-token">
            <div>
                <div on:click={() => selectMode(APP_MODE.NORMAL)} class="flex-auto">
                    <dt>{APP_MODE.NORMAL}</dt>
                </div>
            </div>
            <div>
                <div on:click={() => selectMode(APP_MODE.AGENT)} class="flex-auto">
                    <dt> 🤖🤖🤖{APP_MODE.AGENT}</dt>
                </div>
            </div>
            <div>
                <div on:click={() => selectMode(APP_MODE.DEGEN)} class="flex-auto">
                    <div>
                        <dt>🤑🚀🌕{APP_MODE.DEGEN}</dt>
                    </div>
                </div>
            </div>
        </dl>
    {/if}		
</div>

<style>
    .select {
        cursor: pointer;
    }
	.select-list {
		position: absolute;
        right: 75px;
        top: 60px;
        padding: 8px;
        width: 224px;
	}
    dt:hover {
        background: #6376a3;
    }
</style>