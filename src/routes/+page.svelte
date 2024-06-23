<script lang=ts>
	import LoaderButton from "$lib/components/LoaderButton.svelte";
	import { FileDropzone } from "@skeletonlabs/skeleton";

	let fileLoading = false;


</script>

<p>Welcome! MIDI2Arduino is a tool to convert MIDI files to be played on one of the most accessible Arduino platforms, the Arduino UNO. Specifically, this transpiler converts midi to arduino code using the the Arduino Tone library. Due to the number of hardware timers on the Arduino UNO, only two tones can be generated on one Arduino UNO at a time. This means multiple files and Arduinos may be necessary to play a full MIDI file depending on the song. This transpiler will output the minimum number of code files in a .zip necessary to represent the given mid . To sync the start of multiple Arduinos playback, it is recommended that a single button is wired to all Arduinos and programmed to start playback. Because of this, the outputted files will be txt files so the code can be easily copied rather than Arduino code files.</p>
<FileDropzone accept=".mid" multiple={false} on:file={console.log} name="files">
	<svelte:fragment slot="meta">.mid allowed</svelte:fragment>
</FileDropzone>
<div class="flex space-x-4 justify-center items-center w-full">
	<LoaderButton text="Convert and Download" btnClass="btn btn-primary variant-ghost" bind:loading={fileLoading}/>
</div>