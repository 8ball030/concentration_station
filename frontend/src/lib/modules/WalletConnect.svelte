<script>
// @ts-nocheck

// WalletConnect
import { createWeb3Modal, defaultWagmiConfig } from "@web3modal/wagmi";
import { mainnet, gnosis } from "@wagmi/core/chains";

const projectId = "1b0aad06235a3007b00055160c73fe1d";
const chains = [mainnet, gnosis];
const wagmiConfig = defaultWagmiConfig({
    chains,
    projectId,
    appName: "Web3Modal",
    });
    const modal = createWeb3Modal({ wagmiConfig, projectId, chains });
</script>

<w3m-button label="Connect" />