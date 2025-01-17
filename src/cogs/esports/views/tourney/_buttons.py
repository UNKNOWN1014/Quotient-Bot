from __future__ import annotations


from core import Context
import discord
from utils import regional_indicator as ri, inputs, truncate_string, emote

from ._base import TourneyButton
from models import Tourney

#! create tourney.full_delete() method
#! increase success message limit to 500
#! fake tags maybe
#! disable tourney slotm in delete


class SetTourneyname(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        m = await self.ctx.simple("Enter the new name of the tournament. (`Max 30 characters`)")
        name = await inputs.string_input(self.ctx, delete_after=True)
        await self.ctx.safe_delete(m)
        self.view.record.name = truncate_string(name, 30)

        await self.view.refresh_view()


class RegChannel(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        m = await self.ctx.simple("Mention the channel where you want to take registrations.")
        channel = await inputs.channel_input(self.ctx, delete_after=True)
        await self.ctx.safe_delete(m)

        if await Tourney.filter(registration_channel_id=channel.id).exists():
            return await self.ctx.error(f"Another tourney is running in {channel.mention}.", 4)
        self.view.record.registration_channel_id = channel.id

        await self.view.refresh_view()


class ConfirmChannel(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        m = await self.ctx.simple("Mention the channel where you want me to post registration confirm messages.")
        channel = await inputs.channel_input(self.ctx, delete_after=True)
        await self.ctx.safe_delete(m)

        self.view.record.confirm_channel_id = channel.id

        await self.view.refresh_view()


class SetRole(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        m = await self.ctx.simple("Mention the role you want to give for correct registration.")
        role = await inputs.role_input(self.ctx, delete_after=True)
        await self.ctx.safe_delete(m)

        self.view.record.role_id = role.id

        await self.view.refresh_view()


class SetMentions(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        m = await self.ctx.simple("How many mentions are required for registration? (Max `10`)")
        mentions = await inputs.integer_input(self.ctx, delete_after=True, limits=(0, 10))
        await self.ctx.safe_delete(m)

        self.view.record.required_mentions = mentions

        await self.view.refresh_view()


class SetPingRole(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        m = await self.ctx.simple("Mention the role you want to ping with registration open message.")
        role = await inputs.role_input(self.ctx, delete_after=True)
        await self.ctx.safe_delete(m)

        self.view.record.ping_role_id = role

        await self.view.refresh_view()


class SetSlots(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        m = await self.ctx.simple("How many total slots are there? (Max `15000`)")
        slots = await inputs.integer_input(self.ctx, delete_after=True, limits=(1, 15000))
        await self.ctx.safe_delete(m)

        self.view.record.total_slots = slots

        await self.view.refresh_view()


class SetEmojis(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        ...


class OpenRole(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        m = await self.ctx.simple("Mention the role for which you want to open/close registrations.")
        role = await inputs.role_input(self.ctx, delete_after=True)
        await self.ctx.safe_delete(m)

        self.view.record.open_role_id = role

        await self.view.refresh_view()


class MultiReg(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        self.view.record.multiregister = not self.view.record.multiregister
        await self.ctx.success(
            f"Now users **{'can' if self.view.record.multiregister else 'can not'}** register more than once.", 3
        )
        await self.view.refresh_view()


class TeamCompulsion(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        self.view.record.teamname_compulsion = not self.view.record.teamname_compulsion
        await self.ctx.success(
            f"Now Team Name **{'is' if self.view.record.teamname_compulsion else 'is not'}** required to register.", 3
        )
        await self.view.refresh_view()


class DuplicateTeamName(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        self.view.record.no_duplicate_name = not self.view.record.no_duplicate_name
        await self.ctx.success(
            f"Duplicate team names are now **{'allowed' if self.view.record.no_duplicate_name else 'not allowed'}**.", 3
        )
        await self.view.refresh_view()


class AutodeleteRejected(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        self.view.record.autodelete_rejected = not self.view.record.autodelete_rejected
        await self.ctx.success(
            f"Rejected registrations will **{'be' if self.view.record.autodelete_rejected else 'not be'}** deleted automatically.",
            3,
        )
        await self.view.refresh_view()


class SuccessMessage(TourneyButton):
    def __init__(self, ctx: Context, letter: str):
        super().__init__(emoji=ri(letter))

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        m = await self.ctx.simple(
            "What message do you want me to show for successful registration? This message will be sent to "
            "DM of players who register successfully.\n\n**Current Success Message:**"
            f"```{self.view.record.success_message if self.view.record.success_message else 'Not Set Yet.'}```"
            "\n`Kindly keep it under 500 characters. Enter none to remove it.`",
            image="https://cdn.discordapp.com/attachments/851846932593770496/900977642382163988/unknown.png",
        )

        msg = await inputs.string_input(self.ctx, delete_after=True)
        await self.ctx.safe_delete(m)

        msg = truncate_string(msg, 500)
        if msg.lower().strip() == "none":
            msg = None
            await self.ctx.success("Removed Success Message.", 3)

        elif msg.lower().strip() == "cancel":
            return

        if msg != None:
            await self.ctx.success("Success Message Updated.", 3)

        self.view.record.success_message = msg
        await self.view.refresh_view()


class DeleteTourney(TourneyButton):
    def __init__(self, ctx: Context):
        super().__init__(emoji=emote.trash)

        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        prompt = await self.ctx.prompt(
            "Are you sure you want to delete this tourney?\n\n`This action is not reversible.`"
        )
        if not prompt:
            return await self.ctx.simple("Okay, not deleting.", 3)

        await self.view.record.full_delete()
        await self.ctx.success("Successfully deleted tourney.", 3)
        return await self.view.on_timeout()


class SaveTourney(TourneyButton):
    def __init__(self, ctx: Context):
        super().__init__(style=discord.ButtonStyle.green, label="Save", disabled=True)
