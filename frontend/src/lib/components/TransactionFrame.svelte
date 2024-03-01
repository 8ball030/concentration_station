<script>
    import {transactionLink} from '$lib/stores'
    /**
	 * @type {string}
	 */
     let srcLink;

     transactionLink.subscribe((value) => {
		srcLink = value;
	});
</script>

<div class="bg-secondary-300 text-primary-800 p-4"> 
    <dl class="list-dl">
        <div>
            <span class="flex-auto">
                <dt class="text-primary-900 font-bold">Explorer Link</dt>
                <dd><a href={srcLink}>{srcLink}</a></dd>
            </span>
        </div>
        <div>
            <span class="flex-auto">
                <dt class="text-primary-900 font-bold">Transaction Hash</dt>
                <dd>0x20d0fda3b4bfbac76ed7d9fe9f6b669b50ad3e94d6a1bacc047584afe9f7ef53</dd>
            </span>
        </div>
        <div>
            <span class="flex-auto">
                <button class="chip variant-soft hover:variant-filled">
                    <span> ✅ </span>
                    <span class="font-bold text-primary-900">Success</span>
                </button>
            </span>
        </div>
    </dl>
</div>