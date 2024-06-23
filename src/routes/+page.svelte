<script lang="ts">
	import LoaderButton from "$lib/components/LoaderButton.svelte";
	import { FileDropzone } from "@skeletonlabs/skeleton";

	let fileLoading = false;
	let uploadedFile: File | null = null;

	let files: FileList;

	async function handleFile(event: Event) {
		if(files.length > 0) {
			uploadedFile = files[0];
			console.log("Uploaded file:", uploadedFile);
		}
	}

	async function convertAndDownload() {
		if (!uploadedFile) {
			alert("Please upload a MIDI file first.");
			return;
		}

		fileLoading = true;

		try {
			const formData = new FormData();
			formData.append('file', uploadedFile);

			const response = await fetch('/api/convert', {
				method: 'POST',
				body: formData
			});

			if (!response.ok) {
				throw new Error('Failed to convert MIDI file.');
			}

			const blob = await response.blob();
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.style.display = 'none';
			a.href = url;
			a.download = 'output.zip';
			document.body.appendChild(a);
			a.click();
			window.URL.revokeObjectURL(url);
		} catch (error) {
			console.error("Error converting MIDI file:", error);
			alert("An error occurred while converting the MIDI file. Please try again.");
		} finally {
			fileLoading = false;
		}
	}
</script>

<p>Welcome! MIDI2Arduino is a tool to convert MIDI files to be played on one of the most accessible Arduino platforms, the Arduino UNO. </p>
<p>This transpiler converts midi to arduino code using the the Arduino Tone library. Due to the number of hardware timers on the Arduino UNO, only two tones can be generated on one Arduino UNO at a time. This means multiple files and Arduinos may be necessary to play a full MIDI file depending on the song. This transpiler will output the minimum number of code files in a .zip necessary to represent the given .mid.</p>
<p>To sync the start of multiple Arduinos playback, it is recommended that a single button is wired to all Arduinos and programmed to start playback. Because of this, the outputted files will be txt files so the code can be easily copied rather than Arduino code files.</p>

<FileDropzone accept=".mid" multiple={false} bind:files={files} on:change={handleFile} name="files">
	<svelte:fragment slot="meta">.mid allowed</svelte:fragment>
</FileDropzone>

<div class="flex space-x-4 justify-center items-center w-full">
	<LoaderButton text="Convert and Download" btnClass="btn btn-primary variant-ghost" bind:loading={fileLoading} onClick={convertAndDownload}/>
</div>
